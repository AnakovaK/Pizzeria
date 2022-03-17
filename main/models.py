from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


def pizza_image_directory_pass(instance, filename):
    return f'media/{instance.id}_{filename}'


class Pizza(models.Model):
    """
    Класс для хранения единицы вида пиццы и ее полное описание.

    :param author: Персонал, кто добавил этот вид пиццы в базу данных
    :param name: Название пиццы
    :param description: Описание пиццы
    :param image: Картинка
    :param created_at: Точное время добавления вида пиццы
    :param price: Цена
    :param rating: Рейтинг пиццы (добавляется вручную)
    :param type: Один из четырех типов (TYPE_VARIANTS) - с курицей/с говядиной/с колбасой/вегетарианская
    """
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

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Customer(models.Model):
    """
    Модель покупателя/персонала. Модель, добавляющая больше функций и параметров к базовому классу User.

    :param user: Пользователь, к которому относится модель покупателя/персонала.
    :type user: :class:`~User`
    :param name: Имя покупателя/персонала
    :param bonus_points: Бонусные очки, которые пользователь получает за совершенную покупку.
    :type bonus_points: int
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    bonus_points = models.IntegerField(default=0, blank=True)

    @receiver(post_save, sender=User)
    def create_customer_from_user(sender, instance, created, **kwargs):
        """
        Метод создания покупателя сразу после того, как пользователь (User) регистрируется на сайте.
        """
        if created:
            Customer.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_customer(sender, instance, **kwargs):
        """
        Метод работает в паре с методом создания покупателя. Сохраняет в базе данных "покупателя".
        """
        instance.customer.save()


class Order(models.Model):
    """
    Модель одного заказа.

    :param customer: Пользователь, к которому относится модель покупателя/персонала.
    :type customer: :class:`~Customer`
    :param date_ordered: Дата, когда заказ был подтвержден и обработан.
    :param complete: Показывает, завершен заказ или нет (добавлен ли он в базу данных после успешной оплаты и получения адреса получателя)
    :type complete: bool
    :param transaction_id: ID перевода (работает в связке с PayPal)
    """
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def get_cart_total(self):
        """
        Метод подсчета суммы всего заказа.
        """
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        """
        Метод подсчета количество товаров заказе. В частности используется для показания количества товаров над корзиной покупок.
        """
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_bonus_points(self):
        """
        Метод подсчета бонусных очков за оформление заказа.
        """
        orderitems = self.orderitem_set.all()
        total = int(sum([item.get_total for item in orderitems]) * 0.05)
        return total


class OrderItem(models.Model):
    """
    Модель одного товара в заказе (чтобы он отображался как один товар с увеличивающимся количеством при добавлении нового товара в ассортименте, а не отдельными строчками в Order).

    :param pizza: Товар - пицца.
    :type pizza: :class:`~Pizza`
    :param order: Заказ, к которому относится товар.
    :type order: :class:`~Order`
    :param quantity: Количество товаров одного вида в заказе.
    :type quantity: int
    :param date_added: Дата, когда заказ был подтвержден и обработан.
    """
    pizza = models.ForeignKey(Pizza, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        """
        Метод подсчета суммы только товара одного вида.
        """
        total = self.pizza.price * self.quantity
        return total


class OrderData(models.Model):
    """
    Модель данных об оформленном заказе.

    :param address: Адрес заказчика.
    :param phone: Телефон заказчика.
    """
    address = models.TextField()
    phone = models.TextField()
