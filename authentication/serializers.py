from rest_framework import serializers
from .models import User




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)



    class Meta:
        model = User
        fields = ['uid', 'email', 'password']

    def validate(self, attrs):
        return attrs   