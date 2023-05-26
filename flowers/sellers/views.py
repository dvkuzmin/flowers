from rest_framework import generics
from .models import User
from .serializers import SellerSerializer


class SellerListAPIView(generics.ListAPIView):
    queryset = User.objects.filter(is_seller=True)
    serializer_class = SellerSerializer
