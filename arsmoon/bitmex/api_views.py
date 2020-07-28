import bitmex
from django.http import JsonResponse
from rest_framework import status, mixins
from rest_framework.response import Response
from arsmoon.bitmex.models import Order, Account
from rest_framework.viewsets import GenericViewSet
from arsmoon.bitmex.serializers import OrderSerializer, CreateOrderSerializer


class OrderBitmexViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
                        mixins.CreateModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    account = None

    def dispatch(self, request, *args, **kwargs):
        if 'account' in self.request.GET:
            self.account = Account.objects.filter(name=self.request.GET['account']).first()
        if not self.account:
            return JsonResponse(
                {'error': 'No account with this name'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer

        return self.serializer_class


    def get_queryset(self, *args, **kwargs):
        return Order.objects.filter(account=self.account)


    def retrieve(self, request, *args, **kwargs):
        """
        **Retrieve Order instance **

        ####**Allowed Methods**:
        ###### - GET

        #### **GET**:
        ###### URL: **api/order/{id}/**

        """
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Cancel order in bitmex by pk

        ####**Allowed Methods**:
        ###### - DELETE

        #### **DELETE**:
        ###### URL: **api/order/{order_id}/**

        #### SUCCESS RESPONSE:
        ```json
        no content
        {status_code: 204}
        ```
        """
        instance = self.get_object()
        try:
            client = bitmex.bitmex(test=True, api_key=self.account.api_key, api_secret=self.account.api_secret)

            client.Order.Order_cancel(orderID=instance.orderID).result()
        except Exception as e:
            message = str(e) if str(e) else 'Something went during Order deletion'
            return Response(
                {'non_field_errors': [message]},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(account=self.account)

    def create(self, request, *args, **kwargs):
        """
        **Create Order in Bitmex**
        ####**Allowed Methods**:
        ###### - POST
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            message = str(e) if str(e) else 'Something went wrong'
            return Response(
                {'non_field_errors': [message]},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
