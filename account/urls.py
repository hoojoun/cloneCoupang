from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.UpdatedLoginView.as_view(template_name="shops/login.html"), name='login'),
    path('loginSeller/', views.UpdatedLoginView.as_view(template_name="shops/loginSeller.html"), name='loginSeller'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('signupSeller/', views.signup_seller, name='signupSeller'),
    # path('login/',views.JWTLoginView.as_view()),
    # path('signup/',views.JWTSignupView.as_view()),
    #
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
