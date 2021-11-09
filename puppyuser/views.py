from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import PupUserSerializer,OwnerPuppiesSerializer, NearbySerializer, \
                        AppointmentsSerializer, RatingSerializer, SingleProfileSerializer, \
                            PuppiesLocationSerializer
from .models import PupUser, Puppy, Appointment, Rating
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.shortcuts import render, get_object_or_404
from django.utils.dateparse import parse_datetime

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            return request.method in SAFE_METHODS

class PupUserSerializerView(viewsets.ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = PupUser.objects.all()
    serializer_class = PupUserSerializer

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user=self.request.user)
        return PupUser.objects.none()

class OwnerPuppiesSerializerView(viewsets.ModelViewSet):
    queryset = Puppy.objects.all()
    serializer_class = OwnerPuppiesSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(owner__user = user)
        else:
            return self.queryset.none()
    def create(self, request, *args, **kwargs):
        owner = request.data.get('owner')
        currentUser = get_object_or_404(PupUser, id = owner)
        if currentUser.user == self.request.user:
            super().create(request, *args, **kwargs)
            return Response({'message':"Puppy added"}, status=200)
        else:
            return Response({'message':"Incorrect owner id"}, status=404)

class GetNearOwnersView(viewsets.ModelViewSet):
    queryset = PupUser.objects.all()
    serializer_class = PupUserSerializer
    permission_classes = [ReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.action == 'list'\
        and self.user.userTypes == "Renter":
            return self.queryset.filter(userType = "Owner")
        else:
            return self.queryset.none()
    def list(self,request):
        queryset = PupUser.objects.get(user = request.user)
        latitude, longitude = queryset.latitude, queryset.longitude
        obj = PupUser.objects.filter(latitude__gt=latitude - 3, latitude__lt=latitude + 3,
                         longitude__gt=longitude - 3, longitude__lt=longitude + 3,
                         userType = "Owner")[:10]
        return Response(NearbySerializer(obj, many = True).data)

class GetAppointmentsView(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentsSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.action not in ['list', 'partial_update', 'create','post']:
            return self.queryset.none()
        currentUser = PupUser.objects.get(user = self.request.user)
        if currentUser.userType == "Owner":
            return self.queryset.filter(puppy__owner__user = self.request.user,
        puppy__owner__userType = "Owner" )
        if currentUser.userType == "Renter":
            return self.queryset.filter(enthusiast__user = self.request.user )

    def partial_update(self,request, *args, **kwargs):
        if (request.data.get('available_from') or request.data.get('available_until')):
            available_from = request.data.get('available_from')
            available_until = request.data.get('available_until')
            PupUser.objects.filter(user = self.request.user, userType = "Owner" ).update(
                available_from = available_from, available_until = available_until
            )
            return Response({"message":"Timeslots updated"})
        return super().partial_update(request, *args, **kwargs)
    def create(self,request, *args, **kwargs):
        currentUser = PupUser.objects.get(user = request.user)
        if currentUser.userType == "Owner":
            return Response({"Message":"Owner can't make appointments"}, status = 404)
        timeslot = request.data.get('timeslot')
        date = parse_datetime(request.data.get('date'))
        enthusiast = PupUser.objects.get(id = request.data.get('enthusiast'))
        puppy = Puppy.objects.get(id = request.data.get('puppy'))
        newApp = Appointment.objects.create(
            timeslot = timeslot ,date = date,enthusiast = enthusiast,puppy = puppy)
        return Response({"Message":"Done"}, status = 200)


class GetOwnerRatingsView(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [ReadOnly]
    def get_queryset(self):
        if self.action not in ['list', 'get']:
            return self.queryset.none()

        return self.queryset.filter(toPuppy__owner__user = self.request.user,
        toPuppy__owner__userType = "Owner" )

class GetRenterRatingsView(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.action not in ['list', 'get', 'create', 'partial_update', 'put']:
            return self.queryset.none()

        return self.queryset.filter(fromUser__user = self.request.user,
        fromUser__userType = "Renter" )

    def partial_update(self, request, *args, **kwargs):

        return super().partial_update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        text = request.data.get('text')
        score = request.data.get('score')
        fromUser = request.data.get('fromUser')
        toPuppy = request.data.get('toPuppy')

        puppy = Puppy.objects.get(id = toPuppy)
        fromUser = PupUser.objects.get(id = fromUser)

        obj = Rating.objects.create(text = text, score = score, fromUser = fromUser,toPuppy = puppy )
        return Response({"message":"Rating Added"})

class GetUserView(viewsets.ModelViewSet):
    queryset = PupUser.objects.all()
    serializer_class = SingleProfileSerializer
    permission_classes = [ReadOnly]

    def get_queryset(self):
        print(self.action)
        if self.action not in ['retrieve', 'get']:
            return self.queryset.none()

        return self.queryset
    def retrieve(self,request, pk):
        obj = get_object_or_404(PupUser,user__username = pk)
        puppiesObj = Puppy.objects.filter(owner = obj)
        puppies = OwnerPuppiesSerializer(puppiesObj, many=True, read_only = True).data
        ratingsObj = Rating.objects.filter(toPuppy__owner = obj)
        ratings = RatingSerializer(ratingsObj, many=True,  read_only = True).data
        resp = SingleProfileSerializer(obj).data
        return Response({'user':resp, 'puppies': puppies, 'ratings':ratings})
class GetPuppyView(viewsets.ModelViewSet):
    queryset = Puppy.objects.all()
    serializer_class = PuppiesLocationSerializer
    # permission_classes = [ReadOnly]

    def get_queryset(self):
        print(self.action)
        if self.action not in ['retrieve', 'get', 'list']:
            return self.queryset.none()

        return self.queryset
    def list(self, request):
        breed = request.query_params.get('breed')
        preferences = request.query_params.get('preferences')
        ageDescending = request.query_params.get('ageDescending')
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')
        if latitude and longitude:
            longitude = float(longitude)
            latitude = float(latitude)
        if breed:
            self.queryset = self.queryset.filter(breed__icontains = breed)
        if preferences:
            self.queryset = self.queryset.filter(description__icontains = preferences)
        if longitude and latitude:
            self.queryset = self.queryset.filter(owner__latitude__gt=latitude - 3,
                     owner__latitude__lt=latitude + 3,
                         owner__longitude__gt=longitude - 3, owner__longitude__lt=longitude + 3,
                         owner__userType = "Owner")
        return Response(PuppiesLocationSerializer(self.queryset, many=True, read_only=True).data)
