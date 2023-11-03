from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Person


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff')

class PersonSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Person
        fields = ('id', 'user', 'sex', 'age', 'status', 'discord_account', 'country')
