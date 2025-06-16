from django.contrib.auth.models import User
from rest_framework import serializers
from .models import PlayerProfile, InventoryItem, Friend, PlayerAsset

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        PlayerProfile.objects.create(user=user)
        return user

class PlayerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerProfile
        fields = ['level', 'xp', 'settings']

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'

class PlayerAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerAsset
        fields = ['id', 'file']
