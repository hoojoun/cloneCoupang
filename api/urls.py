from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from api.views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', ProductList.as_view(), name='api'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('signup/', SignUpAPIView.as_view(), name='signup_api'),
    path('login/', LoginAPIView.as_view(), name='login_api'),
    path('logout/', LogoutAPIView.as_view(), name='logout_api'),

    path('auth/refresh/', TokenRefreshView.as_view()),
]
