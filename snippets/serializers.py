from rest_framework import serializers
from snippets.models import Snippet
#, Untis
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework import serializers
from rest_auth.models import TokenModel
from rest_auth.serializers import UserDetailsSerializer as DefaultUserDetailsSerializer

class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ['id', 'owner', "data"]

    

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    
    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']

"""
class UntisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'owner', "data"]
"""