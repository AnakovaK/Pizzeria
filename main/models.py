from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def pizza_image_directory_pass(instance, filename):
    return f'media/{instance.id}_{filename}'


class Pizza(models.Model):
    TYPE_VARIANTS = (
        (0, 'С курицей'),
        (1, 'С говядиной'),
        (2, 'С колбасой'),
        (3, 'Вегетарианская')
    )
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    created_at = models.DateTimeField(default=timezone.now)
    price = models.IntegerField()
    rating = models.IntegerField()
    type = models.IntegerField(default=0, choices=TYPE_VARIANTS)

    @staticmethod
    def get_all():
        return Pizza.objects.all()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)


class OrderItem(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
