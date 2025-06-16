from django.contrib import admin
from .models import PlayerProfile, InventoryItem, Friend, PlayerAsset

@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp')

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('player', 'itemId', 'quantity')

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('player', 'friend')

@admin.register(PlayerAsset)
class PlayerAssetAdmin(admin.ModelAdmin):
    list_display = ('player', 'file')
