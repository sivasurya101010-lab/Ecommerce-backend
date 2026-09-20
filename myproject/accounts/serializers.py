
from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'email']

    def create(self, validated_data):
       password=validated_data.pop('password')

       user=User(**validated_data)

       user.set_password(password)

       user.save()

       return user
