from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import login as authlogin
from account.models import CustomUser
from shops.models import Products, Review
from rest_framework import viewsets
from rest_framework.response import Response
from api.serializers import UserSerializer, SignUpSerializer, ReviewSerializer, ProductDetailSerializer
from rest_framework import status
from dj_rest_auth.urls import LoginView, LogoutView
from django.conf import settings
from django.contrib.auth import logout as django_logout
from dj_rest_auth.jwt_auth import unset_jwt_cookies
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.paginator import Paginator


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class ProductList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shops/landing_api.html'

    def get(self, request):
        page = request.GET.get('page', '1')
        products = Products.objects.order_by('-id')
        paginator = Paginator(products, 10)
        page_obj = paginator.get_page(page)
        context = {'products': page_obj}
        return Response(context)


class ProductDetail(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shops/productDetail_api.html'

    def get(self, request, pk):
        queryset = Products.objects.get(id=pk)
        serializer_class = ProductDetailSerializer(queryset)
        product = {'product': serializer_class}
        return Response(product)


class SignUpAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shops/signup_api.html'

    def get(self, request):
        response = render(request, 'shops/signup_api.html')
        return response

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            authlogin(request, user)
            response.set_cookie("access", access_token, httponly=True)
            response.set_cookie("refresh", refresh_token, httponly=True)
            res = redirect('api')
            res.cookies = response.cookies
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(LoginView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'shops/login_api.html'

    def get(self, request):
        response = render(request, 'shops/login_api.html')
        return response

    def get_response(self):
        response = redirect('api')
        response.cookies = super().get_response().cookies
        return response


class LogoutAPIView(LogoutView):
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = redirect('api')
        unset_jwt_cookies(response)
        if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
            try:
                token = RefreshToken(request.data.get('refresh'))
                token.blacklist()
            except KeyError:
                response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
