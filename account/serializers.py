# from rest_framework_simplejwt import serializers
# from .models import CustomUser
#
# class UserJWTSignupSerializer(serializers.ModelSerializer):
#     id = serializers.CharField(
#         required=True,
#         wite_only=True,
#         max_length=20,
#     )
#     password = serializers.CharField(
#         required=True,
#         wite_only=True,
#         style={'input_type': 'password'}
#     )
#
#     class Meta(object):
#         model = CustomUser
#         fields = ['id', 'password']
#
#     def save(self, request):
#         user = super().save()
#
#         user.id = self.validated_data['id']
#         user.set_password(self.validated_data['password'])
#         user.save()
#
#         return user
#
#     def validate(self, data):
#         id = data.get('id', None)
#         if CustomUser.objects.filter(id=id).exists():
#             raise serializers.ValidationError("user already exists")
#         return data
