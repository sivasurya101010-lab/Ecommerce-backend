from django.contrib.auth.models import User
from rest_framework import serializers

class RegsiterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'email']

    def create(self, validated_data):
       user=User(**validated_data)

       user.set_password(validated_data['password'])

       user.save()

       return user

