from django.contrib.auth.models import User
from django.db import models

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    settings = models.JSONField(default=dict)

class InventoryItem(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    itemId = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    metadata = models.JSONField(default=dict)

class Friend(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')

class PlayerAsset(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assets/')
