from rest_framework import serializers
from snippets.models import Snippet


#Serializer to save Objects automatically in Database
class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ['id', 'owner', "data"]

