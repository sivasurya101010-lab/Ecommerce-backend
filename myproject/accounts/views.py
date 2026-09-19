from .serializers import RegsiterSerializer
from rest_framework import generics


class RegisterView(generics.CreateAPIView):

    serializer_class=RegsiterSerializer

