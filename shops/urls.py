from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.landing, name='landing'),
                  path('productRegister/', views.product_register, name='product_register'),
                  path('product/<int:pk>/', views.product_detail, name='product_detail'),
                  path('product/<int:pk>/review/', views.review, name='review'),
                  path('product/<int:pk>/<int:pk2>/', views.review_to_review, name='review_to_review'),
                  path('product/<int:pk>/cert/', views.add_cert, name="add_cert"),
                  path('cert/', views.cert, name="cert"),
                  path('certbuy/', views.buy_cert, name="certbuy"),
                  path('report/review/<str:pk>/<int:pk2>/<int:pk3>/', views.report_review, name='report_review'),
                  path('report/reviewtoreview/<str:pk>/<int:pk2>/<int:pk3>/', views.report_review_to_review,
                       name='report_reviev_to_review'),
                  path('seller/', views.seller, name="seller"),
                  path('delivery/<int:pk>/', views.delivery, name='delivery')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
