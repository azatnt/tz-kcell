from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contact')
    phone = models.CharField(max_length=150)
    instagram = models.URLField()
    telegram = models.URLField()
