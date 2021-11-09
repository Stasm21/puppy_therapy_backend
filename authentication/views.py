from django.contrib.auth.models import User
from .serializers import RegistrationSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from puppyuser.models import PupUser

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def create(self, request, **kwargs):
        validated_data = request.data
        user = User.objects.create(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        puppy_user = PupUser.objects.create(user = user, street_address = validated_data['street_address'],
            city = validated_data['city'],state = validated_data['state'],
            zip_code = validated_data['zip_code'],
            userType = validated_data['user_type'], latitude = validated_data['latitude'],
            longitude = validated_data['longitude']
            )
        puppy_user.save()
        
        return Response("User Created")

