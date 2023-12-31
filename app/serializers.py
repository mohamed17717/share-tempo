from rest_framework import serializers

from app import models
from app.serializer_custom_fields import SallaSubscriptionPlanDurationField

def PROMPT_TYPES():
    from app import controllers
    return controllers.ChatGPTProductPromptGenerator.get_prompt_types()

class SallaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SallaUser
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated': {'read_only': True},
            'password': {'read_only': True},
        }


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }


class SallaStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SallaStore
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated': {'read_only': True},
        }


class ChatGPTResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChatGPTResponse
        fields = '__all__'


class UserPromptSerializer(serializers.ModelSerializer):
    chat_gpt_response = ChatGPTResponseSerializer(read_only=True)
    class Meta:
        model = models.UserPrompt
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }


class SallaUserSubscriptionPayloadSerializer(serializers.Serializer):
    plan_type = serializers.CharField() 
    plan_name = serializers.CharField()
    plan_period = SallaSubscriptionPlanDurationField(allow_null=True)
    price = serializers.FloatField()

    start_date = serializers.DateTimeField(write_only=True, allow_null=True, required=False)
    end_date = serializers.DateTimeField(write_only=True, allow_null=True, required=False)

    def validate(self, attrs):
        from datetime import datetime, timedelta

        if attrs.get('start_date') is None:
            attrs['start_date'] = datetime.now()
        if attrs.get('end_date') is None:
            attrs['end_date'] = datetime.now() + timedelta(days=365*10)

        if attrs.get('plan_period') is None and attrs.get('start_date') and attrs.get('end_date'):
            attrs['plan_period'] = attrs['end_date'] - attrs['start_date']
        return super().validate(attrs)


class ProductEndpointParamsSerializer(serializers.Serializer):
    STATUS_CHOICES = ('hidden', 'sale', 'out')

    category = serializers.CharField(required=False, max_length=100)
    keyword = serializers.CharField(required=False, max_length=100)
    page = serializers.IntegerField(required=False, default=1)
    per_page = serializers.IntegerField(required=False, default=10)
    status = serializers.ChoiceField(required=False, choices=STATUS_CHOICES)


class ChatGPTResponseSerializer(serializers.Serializer):
    id = serializers.CharField(write_only=True, required=False)
    object = serializers.CharField(write_only=True, required=False)
    created = serializers.CharField(write_only=True, required=False)
    model = serializers.CharField(write_only=True, required=False)
    usage = serializers.DictField(write_only=True)
    choices = serializers.ListField(write_only=True, child=serializers.DictField())

    prompt = serializers.CharField()

    total_tokens = serializers.IntegerField(source='usage.total_tokens', read_only=True)
    answer = serializers.SerializerMethodField(read_only=True)
    full_response = serializers.DictField(source='*', read_only=True)

    def get_answer(self, obj):
        return obj['choices'][0]['text'].strip().strip('"')

    def save(self, **kwargs):
        return models.ChatGPTResponse.objects.create(**self.data)


class ProductGetDescriptionPOSTBodySerializer(serializers.Serializer):
    # Those will be used as values in the chatgpt templates
    product_id = serializers.CharField(required=True)
    product_name = serializers.CharField(required=True)
    product_description = serializers.CharField(required=False, allow_null=True)
    product_seo_title = serializers.CharField(required=False, allow_null=True)
    # brand_name = serializers.CharField(required=False, allow_null=True)
    keywords = serializers.CharField(required=True)

    prompt_type = serializers.ChoiceField(required=True, choices=PROMPT_TYPES())


class ProductListHistoryPOSTBodySerializer(serializers.Serializer):
    product_id = serializers.CharField(required=True)
    prompt_type = serializers.ChoiceField(required=True, choices=PROMPT_TYPES())


class ProductUpdatePOSTBodySerializer(serializers.Serializer):
    # product_id = serializers.CharField(required=True)
    # prompt_type = serializers.ChoiceField(required=True, choices=PROMPT_TYPES())
    # new_value = serializers.CharField(required=True)
    prompt_id = serializers.CharField(required=True)


class ProductUpdateManuallyPOSTBodySerializer(serializers.Serializer):
    product_id = serializers.CharField(required=True)
    prompt_type = serializers.ChoiceField(required=True, choices=PROMPT_TYPES())
    new_value = serializers.CharField(required=True)


class LoginPOSTBodySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class SallaWebhookLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SallaWebhookLog
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }


