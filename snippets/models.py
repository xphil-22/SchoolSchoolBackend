from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    data = models.JSONField(blank=True)
    
    class Meta:
        ordering = ['created']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    snippetID = models.IntegerField(null=True)
    untisUsername = models.CharField(blank=True, max_length=50)
    untisPassword = models.CharField(blank=True, max_length=50)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

"""
class Untis(models.Model):
    Untisdata = models.JSONField(blank=True)
"""   