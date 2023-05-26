from django.urls import path, include
from .views import SellerListAPIView

sellers_urls = [
    path('sellers/', SellerListAPIView.as_view(), name='sellers-list'),
]

urlpatterns = [
    path('v1/', include(sellers_urls))
]
