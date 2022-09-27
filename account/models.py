from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=12)
    activate = models.BooleanField(null=True)
    history=HistoricalRecords()

class CustomSeller(models.Model):
    CustomUser = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    businessType = models.CharField(max_length=100)

    def __str__(self):
        return self.CustomUser.username


class Consent(models.Model):
    name = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50, null=True)
    content = models.TextField(null=True)
    isUser = models.BooleanField(null=True)
    activate = models.BooleanField(null=True)

    def __str__(self):
        return self.title


class UserConsent(models.Model):
    cid = models.ForeignKey(Consent, on_delete=models.CASCADE, null=True)
    ccheck = models.BooleanField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

class BlacklistLog(models.Model):
    content = models.TextField(null=True)
