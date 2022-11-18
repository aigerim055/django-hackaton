from rest_framework import serializers

from .models import (
    Order, 
    OrderItems
)

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
        order.total_sum = total_sum
        order.save()
        return order