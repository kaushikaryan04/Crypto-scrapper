
from rest_framework import serializers
from .models import Job, Coin, CoinOutput, Link

# class ContractSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Contract
#         fields = ['name', 'address']

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['name', 'link']

class CoinOutputSerializer(serializers.ModelSerializer):
    official_links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = CoinOutput
        fields = [
            'price', 'price_change', 'market_cap', 'market_cap_rank', 'volume',
            'volume_rank', 'volume_change', 'circulating_supply', 'total_supply',
            'diluted_market_cap', 'official_links'
        ]

class CoinSerializer(serializers.ModelSerializer):
    output = CoinOutputSerializer(read_only=True)

    class Meta:
        model = Coin
        fields = ['name', 'output']

class JobSerializer(serializers.ModelSerializer):
    tasks = CoinSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = ['job_id', 'tasks']
