from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)


class Post(models.Model):
    plate = models.CharField(max_length=9)
    description = models.TextField()
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default="В работе")

    # пример создания связи Many-to-many
    # recipients = models.ManyToManyField("User", related_name="emails_received")

    # пример создания поля True or False
    # archived = models.BooleanField(default=False)