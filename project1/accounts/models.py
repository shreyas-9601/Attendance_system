import os
from django.contrib.auth.models import AbstractUser
from django.db import models


def path_and_rename(instance, filename):
    upload_to = 'images'
    ext = filename.split('.')[-1]
    # get filename
    filename = '{}.{}'.format(instance.username, ext)
    return os.path.join(upload_to, filename)


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to=path_and_rename, default="", blank=False, null=False)
    division = models.CharField(max_length=5, default='')
