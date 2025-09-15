""" Models to extend the django user model,
    adding avatars and decorations
"""
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Decoration(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/', null=False, blank=False)
    cost = models.IntegerField(default = 25)

    def __str__(self):
        return self.name

class Avatar(models.Model):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='images/', null=False, blank=False)
    cost = models.IntegerField(default = 25)

    def __str__(self):
        return self.name

class ExtendedUser(AbstractUser):

    avatar = models.ForeignKey(Avatar, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name='%(class)s_avatar_used')
    #User may not have an avatar to begin with, so can be null
    decoration = models.ForeignKey(Decoration, blank=True, null=True, on_delete=models.SET_NULL,
                                    related_name='%(class)s_decoration_used')
    #User may not have a decoration to begin with, so can be null
    email = models.EmailField(null=False, blank=False)
    #User must have an email to log in, so cannot be null
    inventoryAvatar = models.ManyToManyField(Avatar, blank=True,
                                             related_name='%(class)s_avatars_stored')
    #Inventory starts empty, so can be blank
    inventoryDecoration = models.ManyToManyField(Decoration, blank=True,
                                                 related_name='%(class)s_decorations_stored')
    #Inventory starts empty, so can be blank
    spentPoints = models.IntegerField(default = 0)

    def __str__(self):
        return self.username

    def points(self):
        points = PointsAwarded.objects.filter(user = self)
        total = 0

        for i in points:
            total += i.points

        return total - self.spentPoints

# Model to track when a user recieves points
class PointsAwarded(models.Model):
    user = models.ForeignKey(ExtendedUser, on_delete = models.CASCADE)
    points = models.IntegerField()
    time = models.DateTimeField(auto_now_add = True)

class Friend(models.Model):
    users = models.ManyToManyField(ExtendedUser)
    current_user = models.ForeignKey(ExtendedUser, related_name='owner',
                                     null=True, on_delete= models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

class FriendRequest(models.Model):
    # store the user that has sent the request
    sent_from = models.ForeignKey(ExtendedUser,
                                  related_name="requests_sent", on_delete= models.CASCADE)
    # store the user that has received the request
    sent_to = models.ForeignKey(ExtendedUser,
                                related_name="requests_received", on_delete= models.CASCADE)

#https://medium.com/@devsumitg/revolutionize-your-user-experience-creating-real-time-notifications-with-django-channels-18053b958fb6#
class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.CharField(max_length=100)
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=datetime.now)
