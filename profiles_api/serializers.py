from rest_framework import serializers
from rest_framework.utils import field_mapping

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """ Make a serializer to test apiview """
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serialize user profile object"""

    class Meta:
        model = models.UserProfile
        fields = ('id', 'name','email', 'password') # show fields 
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    # override django create for this serializer
    def create(self, validated_data):
        """create and return user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
        )

        return user


class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serialize ProfileFeedItems"""


    class Meta:
        model = models.ProfileFeedItem
        fields = ('id','user_profile','status_text','created_on')
        # id and created_on are read-only by default
        # we make user_profile read only because we will use it for auth

        extra_kwargs = {
            'user_profile': {
                'read_only': True
            }
        }
        
