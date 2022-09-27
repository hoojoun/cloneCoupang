from django.db import models
from account.models import CustomSeller, CustomUser


# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    seller = models.ForeignKey(CustomSeller, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)


class Cert(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    active = models.BooleanField(null=True)


class PurchaseHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    Delivery = models.BooleanField(blank=False, null=True)


class Review(models.Model):
    title = models.CharField(max_length=50, null=True)
    content = models.TextField(null=True)
    starRating = models.IntegerField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)


class ReviewToReview(models.Model):
    content = models.TextField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)


class Report(models.Model):
    report_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='report_user')
    reported_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='reported_user')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True)
    reviewtoreview = models.ForeignKey(ReviewToReview, on_delete=models.CASCADE, null=True)
    content = models.TextField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["report_user", "review"], name="한 번만 신고",
            )
        ]


class BlackListHistory(models.Model):
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='admin')
    blacklist = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='blacklist')
    content = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
