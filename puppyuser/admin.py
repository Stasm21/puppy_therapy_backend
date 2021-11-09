from django.contrib import admin
from .models import PupUser,Puppy, Appointment, Rating

admin.site.register(PupUser)
@admin.register(Puppy)
class PuppyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ['name']
admin.site.register(Appointment)
admin.site.register(Rating)


