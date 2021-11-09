from rest_framework import serializers
from django.contrib.auth.models import User
from .models import PupUser, Puppy ,Appointment, Rating

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password","user_permissions","is_staff","groups",'is_superuser')

class PupUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = PupUser
        fields = "__all__"

class NearbySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(source = "get_user")
    class Meta:
        model = PupUser
        fields = "__all__"
    
    def get_user(self, obj):
        user = User.objects.get(id = obj.user_id)
        return UserSerializer(user).data

class OwnerPuppiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Puppy
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    toPuppy = OwnerPuppiesSerializer()
    fromUser = PupUserSerializer()
    owner = PupUserSerializer(source = "toPuppy.owner")

    class Meta:
        model = Rating
        fields = "__all__"

class AppointmentsSerializer(serializers.ModelSerializer):
    puppy = OwnerPuppiesSerializer()
    enthusiast = PupUserSerializer()
    owner = PupUserSerializer(source= "puppy.owner")
    class Meta:
        model = Appointment
        fields = "__all__"


class SingleProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = PupUser
        fields = "__all__"
class PuppiesLocationSerializer(serializers.ModelSerializer):
    owner = PupUserSerializer()
    class Meta:
        model = Puppy
        fields = "__all__"
       
    