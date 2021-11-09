from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from puppyuser.models import PupUser

class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                    UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    street_address = serializers.CharField(write_only=True, required=False)
    city = serializers.CharField(write_only=True, required=False)
    state = serializers.CharField(write_only=True, required=False)
    zip_code = serializers.CharField(write_only=True, required=False)
    rating = serializers.IntegerField(write_only=True, required=False,default=5, initial = 5)
    user_type = serializers.CharField(write_only=True, required=False,default="Owner")

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'street_address',
            'city', 'state', 'zip_code', 'rating','user_type')

    