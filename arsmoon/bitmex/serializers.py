from bravado.exception import HTTPBadRequest

from arsmoon.bitmex.models import Order
from rest_framework import  serializers
import bitmex

ORDER_TYPE = {
    'Buy': 'Buy',
    'Sell': 'Sell'

}

class OrderSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'orderID', 'timestamp', 'volume', 'side', 'price', 'account', 'symbol']

    def get_account(self, instance):
        return instance.account.name


class CreateOrderSerializer(serializers.ModelSerializer):
    side = serializers.ChoiceField(choices=ORDER_TYPE, required=True)
    symbol = serializers.CharField(required=True)
    orderQty = serializers.FloatField(required=True)

    class Meta:
        model = Order
        fields = ['side', 'symbol', 'orderQty']

    def create(self, validated_data):
        try:
            client = bitmex.bitmex(test=True, api_key=validated_data['account'].api_key,
                                   api_secret=validated_data['account'].api_secret)

            result = client.Order.Order_new(symbol=validated_data['symbol'], orderQty=validated_data['orderQty'],
                                            ordType='Market',side=validated_data['side']).result()
            instance = Order.objects.create(
                orderID=result[0]['orderID'],
                symbol=result[0]['symbol'],
                volume=result[0]['orderQty'],
                timestamp=result[0]['timestamp'],
                side=result[0]['side'],
                price=result[0]['price'],
                account=validated_data['account']
            )
            return instance
        except HTTPBadRequest:
            raise serializers.ValidationError('Something went wrong with Order creation')


    def to_representation(self, instance):
        return_serializer = OrderSerializer(instance)
        return return_serializer.data
