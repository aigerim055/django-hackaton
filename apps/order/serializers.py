from rest_framework import serializers

from .models import (
    Order, 
    OrderItems
)
from apps.bio.models import UserProfile

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['book', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_id', 'created_at', 'address', 'total_sum', 'items']

    def create(self, validated_data, *args, **kwargs):
        user = self.context['request'].user
        profile = UserProfile.objects.filter(user=user)

        items = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        order = super().create(validated_data) # Order.objects.create
        total_sum = 0
        orders_items = []
        for item in items:
            orders_items.append(OrderItems(
                order=order,
                book=item['book'],
                quantity=item['quantity']
            ))
            total_sum += item['book'].price * item['quantity']
        OrderItems.objects.bulk_create(orders_items, *args, **kwargs)

        reward = int(profile.values('cashback')[0]['cashback'])
        order.total_sum = total_sum - total_sum*reward/100

        collected_sum = int(profile.values('collected_sum')[0]['collected_sum'])
        collected_sum += order.total_sum

        profile.update(
            collected_sum=collected_sum)

        check_cashback = int(profile.values('collected_sum')[0]['collected_sum']) 
        if check_cashback >= 10000:
            profile.update(
                cashback=5)
        if check_cashback >= 20000:
            profile.update(
                cashback=7)
        if check_cashback >= 30000:
            profile.update(
                cashback=10)

        order.save()
        return order


class OrderHistorySerializer(serializers.ModelSerializer):

    # url = serializers.ReadOnlyField(source='order.get_absolute_url')
    # book = serializers.ReadOnlyField(source='order.book')
    
    class Meta:
        model = Order
        fields = ('order_id', 'address', 'total_sum', 'status', 'created_at', 'books')

