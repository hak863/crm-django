from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_organiser = models.BooleanField(default=True) # this is the default value for the field is_organiser
    is_agent = models.BooleanField(default=False) # this is the default value for the field is_agent

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    
class Lead(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL) #this is the foreign key for the agent model and it is set to null if the agent is deleted
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL) #this is the foreign key for the agent model and it is set to null if the agent is deleted

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email

class Category(models.Model): #new, contracts, contacted, converted, unconverted
    name=models.CharField(max_length=30)


    def __str__(self):
        return self.name


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    
post_save.connect(post_user_created_signal, sender=User)