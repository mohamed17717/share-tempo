import random
import string

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

from rest_framework.exceptions import ValidationError

from app import models
from app import utils
from app.controllers import SallaMerchantReader, SallaAppSettingsReader
from app.serializers import SallaUserSerializer, SallaStoreSerializer, SallaUserSubscriptionPayloadSerializer


@receiver(pre_save, sender=models.Account)
def pull_user(sender, instance, **kwargs):
    created = instance.pk is None
    user_not_exists = instance.user is None

    if created and user_not_exists:
        user_data = SallaMerchantReader(instance).get_user()
        user_data['salla_id'] = user_data.pop('id')

        # user = utils.create_by_serializer(SallaUserSerializer, user_data)
        # instance.user = user
        
        user = models.SallaUser.objects.filter(salla_id=user_data['salla_id']).first()
        if user:
            s = SallaUserSerializer(user, data=user_data)
        else:
            s = SallaUserSerializer(data=user_data)

        s.is_valid(raise_exception=True)
        user = s.save()

        instance.user = user


@receiver(post_save, sender=models.Account)
def pull_store(sender, instance, created, **kwargs):
    if created:
        store_data = SallaMerchantReader(instance).get_store()
        store_data['salla_id'] = store_data.pop('id')
        store_data['user'] = instance.user.pk

        store = models.SallaStore.objects.filter(salla_id=store_data['salla_id']).first()
        if store:
            s = SallaStoreSerializer(store, data=store_data)
        else:
            s = SallaStoreSerializer(data=store_data)

        s.is_valid(raise_exception=True)
        instance = s.save()


@receiver(post_save, sender=models.Account)
def send_password_via_email(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        password = ''.join(random.choices(
            string.ascii_letters+string.digits, k=16))

        user.password = password
        user.save()

        subject = 'مرحبا بك في تفاصيل'
        message = (
            f'مرحبًا {user.name},\n\n'

            'مرحبًا في تطبيق "تفاصيل"! إليك تسجيل الدخول:\n'
            f'- اسم المستخدم: {user.email}\n'
            f'- كلمة المرور: {user.password}\n\n'
            
            'استخدمهما للوصول إلى تطبيق "تفاصيل".\n'
            'للمساعدة، اتصل بفريق الدعم.\n\n'
            
            'نتمنى لك تجربة ممتعة!\n\n'
            
            'https://tafaseel.io/\n\n'
            
            'مع أطيب التحيات،\n'
            '"تفاصيل"\n'
            '---'
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email, ])


@receiver(post_save, sender=models.Account)
def pull_subscription_plan(sender, instance, created, **kwargs):
    if created:
        account = instance

        subscription_response = SallaAppSettingsReader(account).get_subscription()
        payload = subscription_response.get('data')

        if payload and type(payload) is list:
            payload = payload[0]
        else:
            raise ValidationError('Invalid subscripion')

        payload_data = SallaUserSubscriptionPayloadSerializer(data=payload)
        payload_data.is_valid(raise_exception=True)

        subscription = models.SallaUserSubscription(
            user=account.user, payload=payload, **payload_data.data,
        )
        subscription.save()

@receiver(post_save, sender=models.UserPrompt)
def update_plan_balance_is_salla(sender, instance, created, **kwargs):
    from .controllers import SallaWriter
    from datetime import timedelta

    if created and instance.chat_gpt_response is not None:
        subscription = instance.user.subscriptions.filter(is_active=True).last()
        start_date = subscription.created_at
        end_date = subscription.created_at + (subscription.plan_period or timedelta(days=1000)) 

        used_prompts = models.UserPrompt.count_for_user(instance.user, start_date, end_date, gpt=True)
        balance = subscription.gpt_prompts_limit - used_prompts
        
        account = instance.user.account
        SallaWriter(account).balance_update({'balance': balance})

        