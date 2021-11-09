
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import (PupUserSerializerView, OwnerPuppiesSerializerView, GetNearOwnersView,
                GetAppointmentsView, GetOwnerRatingsView, GetRenterRatingsView,GetUserView,
                GetPuppyView
                )
from django.contrib import admin
from django.urls import path, include

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('puppy_user', PupUserSerializerView)
router.register('ownerPuppies', OwnerPuppiesSerializerView)
router.register('getNear', GetNearOwnersView)
router.register('user-profile', GetAppointmentsView)
router.register('ownerReviews', GetOwnerRatingsView)
router.register('renterReviews', GetRenterRatingsView)
router.register('get-user', GetUserView)
router.register('get-puppies', GetPuppyView)

urlpatterns = []
urlpatterns += router.urls
