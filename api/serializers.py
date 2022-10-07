from account.models import CustomUser
from shops.models import *
from rest_framework import serializers


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        name = validated_data.get('name')
        phone = validated_data.get('phone')
        user = CustomUser(
            username=username,
            name=name,
            phone=phone,
        )
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ReviewToReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewToReview
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    reviewtoreviews = ReviewToReviewSerializer(many=True)

    class Meta:
        model = Review
        fields = ("id", "title", "content", "starRating", "user", "reviewtoreviews")


class ProductDetailSerializer(serializers.ModelSerializer):


    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Products
        fields = ("id", "name", "price", "image", "seller", "reviews")
