from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.bio.models import UserProfile
from apps.book.models import Book

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_process', 'Processing'),
        ('canceled', 'Cancelled'),
        ('finished', 'Finished')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='orders'
    )
    books = models.ManyToManyField(
        to=Book,
        through='OrderItems',
    )
    order_id = models.CharField(max_length=58, blank=True)
    address = models.CharField(max_length=200)
    total_sum = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='open')
    confirmation_code = models.CharField(max_length=6, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # reward = models.ForeignKey(
    #     to=UserProfile,
    #     on_delete=models.CASCADE,
    #     related_name='rewards'
    # )

    def __str__(self):
        return f'Order #{self.order_id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.order_id:
            self.order_id = str(self.user.username) + '-' + (str(self.created_at))[5:16].replace(':', '-').replace(' ', '-')
            # self.order_id = ''.join([i for i in self.order_id if i not in '.: -'])
        return self.order_id

    def get_absolute_url(self):
        return reverse("order-detail", kwargs={"pk": self.pk})


class OrderItems(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.RESTRICT,
        related_name='items'
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.RESTRICT,
        related_name='items'
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'