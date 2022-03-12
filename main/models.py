from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


def pizza_image_directory_pass(instance, filename):
    return f'media/{instance.id}_{filename}'
