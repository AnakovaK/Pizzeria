from django.contrib.auth import get_user_model
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
