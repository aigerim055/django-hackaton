from rest_framework import serializers

from .models import (
    Order, 
    OrderItems
)
from apps.bio.models import UserProfile
from apps.account.models import User

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['book', 'quantity']

        # if self.products.quantity  -  добавить проверки


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_id', 'created_at', 'address', 'total_sum', 'items']

    def create(self, validated_data, *args, **kwargs):
        user = self.context['request'].user
        print(user)
        profile = UserProfile.objects.filter(user=user)
        print(profile)

        # user = 
        # super().save(*args, **kwargs)
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
        print(order.total_sum)
        collected_sum = int(profile.values('collected_sum')[0]['collected_sum'])
        collected_sum += order.total_sum
        UserProfile.objects.filter(user=user).update(
        collected_sum=collected_sum,
)
        # print(collected_sum)
        order.save()
        # profile.save()
        print(profile.values('collected_sum')[0]['collected_sum'])
        return order


class OrderHistorySerializer(serializers.ModelSerializer):

    # url = serializers.ReadOnlyField(source='order.get_absolute_url')
    # book = serializers.ReadOnlyField(source='order.book')
    
    class Meta:
        model = Order
        fields = ('order_id', 'address', 'total_sum', 'status', 'created_at', 'books')

