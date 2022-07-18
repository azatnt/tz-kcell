from django.contrib.auth.models import User
from rest_framework import serializers

from main.models import Contact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['phone', 'telegram', 'instagram']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserWithContactSerializer(UserSerializer):
    user_contact = ContactSerializer(read_only=True, many=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['user_contact']


class ContactWithUserSerializer(ContactSerializer):
    user = UserSerializer(read_only=True)

    class Meta(ContactSerializer.Meta):
        fields = ['user'] + ContactSerializer.Meta.fields


class ContactGroupedByUserSerializer(UserSerializer):
    user_contact = ContactSerializer(read_only=True, many=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['user_contact']