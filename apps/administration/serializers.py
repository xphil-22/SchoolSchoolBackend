from rest_framework import serializers
from snippets.models import Snippet
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):  #Serializer to save Objects automatically in Database
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    
    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']