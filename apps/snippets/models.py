from django.db import models
# Create your models here.

#Model to create Objects in Database
class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    data = models.JSONField(blank=True)
    
    class Meta:
        ordering = ['created']
        
  