from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.utils.timezone import now
from rest_framework.parsers import MultiPartParser
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>🎮 Game Backend API</h1><p>The API is running successfully.</p>")

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class ServerTimeView(APIView):
    def get(self, request):
        return Response({'utc': now().isoformat() + 'Z'})

class PlayerDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        profile = PlayerProfile.objects.get(user_id=id)
        return Response(PlayerProfileSerializer(profile).data)

    def put(self, request, id):
        profile = PlayerProfile.objects.get(user_id=id)
        serializer = PlayerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})
        return Response(serializer.errors, status=400)

class InventoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        items = InventoryItem.objects.filter(player_id=id)
        return Response(InventoryItemSerializer(items, many=True).data)

    def post(self, request, id):
        data = request.data.copy()
        data['player'] = id
        item, created = InventoryItem.objects.get_or_create(player_id=id, itemId=data['itemId'])
        item.quantity += int(data.get('qty', 1))
        item.save()
        return Response({'success': True, 'newQty': item.quantity})

class FriendView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        Friend.objects.create(player_id=id, friend_id=request.data['friendUserId'])
        return Response({'success': True})

    def get(self, request, id):
        friends = Friend.objects.filter(player_id=id)
        return Response([
            {
                'userId': f.friend.id,
                'username': f.friend.username,
                'status': 'added'
            } for f in friends
        ])

class AssetUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        asset = PlayerAsset(player_id=id, file=request.FILES['file'])
        asset.save()
        return Response({'assetId': asset.id, 'url': asset.file.url})
