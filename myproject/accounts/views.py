from .serializers import RegisterSerializer
from rest_framework import generics


class RegisterView(generics.CreateAPIView):

    serializer_class=RegisterSerializer

