from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import IntegerField


class PupUser(models.Model):
    USER_CHOICES = [
        ('Owner', 'Owner'),
        ('Renter', 'Renter')]
    street_address = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip_code = models.CharField(max_length=5, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userType = models.CharField(choices=USER_CHOICES,default = "Owner",max_length=20)
    latitude = models.FloatField(default=0, null=True)
    longitude = models.FloatField(default=0, null=True)
    available_from = models.IntegerField(default=0)
    available_until = models.IntegerField(default=24)


    def __str__(self):
        return self.user.first_name
class Puppy(models.Model):
    name = models.CharField(max_length=50 )
    breed = models.CharField(max_length=100, blank=True, null=True)
    age = models.CharField(blank=True, null=True, max_length=50)
    vaccinated = models.BooleanField(default = False)
    description = models.CharField(max_length=1000, blank=True, null=True)
    price = models.IntegerField(default=1)
    image = models.ImageField(null=True)
    owner = models.ForeignKey(PupUser,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.name

class Appointment(models.Model):
    class Meta:
        unique_together = ('puppy', 'date', 'timeslot')
    TIMESLOT_LIST = [[x,f"{x}:00 - {x+1}:00"] for x in range(24)]
    enthusiast = models.ForeignKey(PupUser,on_delete = models.CASCADE, 
                related_name="enthusiast")
    date = models.DateField(help_text="YYYY-MM-DD")
    timeslot = models.IntegerField(choices=TIMESLOT_LIST)
    puppy = models.ForeignKey(Puppy,on_delete = models.CASCADE, related_name="appointment_puppy")
    accepted = models.IntegerField(default = 0)
    def __str__(self):
        return '{} {} {}. Client: {}'.format(self.date, self.time, self.puppy, self.enthusiast)

    @property
    def time(self):
        return self.TIMESLOT_LIST[self.timeslot][1]

class Rating(models.Model):
    score = models.IntegerField(default = 5)
    text = models.TextField(blank=True, null=True)
    toPuppy = models.ForeignKey(Puppy,on_delete = models.CASCADE, related_name="toPuppy")
    fromUser = models.ForeignKey(PupUser,on_delete = models.CASCADE, related_name="fromUser")
    time_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('toPuppy', 'fromUser')
    def __str__(self):
        return f"{self.fromUser.user.first_name} gave {self.score} stars to {self.toPuppy.owner.user.first_name}"
