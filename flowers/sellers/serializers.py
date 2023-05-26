from django.db.models import Sum
from rest_framework import serializers
from .models import User, Transaction


class BuyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    buyers = BuyerSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'buyers']


class SellerSerializer(serializers.ModelSerializer):
    buyers = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'buyers']

    def get_buyers(self, obj):
        lots = obj.flowerlot_set.all()
        buyers = set()
        for lot in lots:
            transactions = lot.transaction_set.all()
            for transaction in transactions:
                buyers.add(transaction.buyer)

        serialized_buyers = BuyerSerializer(buyers, many=True).data
        for buyer_data in serialized_buyers:
            buyer_data['total_purchases'] = Transaction.objects.filter(buyer=buyer_data['id'], lot__seller__id=obj.id).aggregate(total_purchases=Sum('quantity'))['total_purchases']

        return serialized_buyers
