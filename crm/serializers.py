from rest_framework import serializers
from .models import Marketing, CampaignProducts, PaymentDetails, SalesDump, MarketingPlan

class MarketingSerializer(serializers.ModelSerializer):
    client_id = serializers.IntegerField()

    class Meta:
        model = Marketing
        fields = '__all__'


class CampaignProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignProducts
        fields = '__all__'

class PaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetails
        fields = '__all__'


class SalesDumpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesDump
        fields = ['id', 'data', 'created_at']
        read_only_fields = ['id', 'created_at']

class MarketingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingPlan
        fields = '__all__'

        