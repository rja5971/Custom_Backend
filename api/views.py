from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from rest_framework.parsers import MultiPartParser
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .serializers import *


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['message'] = f"Welcome {self.user.username}! You are successfully logged in."
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def home(request):
    return HttpResponse("<h1>🎮 Game Backend API</h1><p>The API is running successfully.</p>")


# ==========================
# JWT API REGISTRATION
# ==========================
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


# ==========================
# Authenticated Greeting (HTML)
# ==========================
class UserGreetingTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'greet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context


# ==========================
# Web Auth Views (HTML login/register)
# ==========================
@csrf_protect
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Successfully logged in!")  # ✅ Add this
            return redirect('greet-user')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


@csrf_protect
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            messages.success(request, "Successfully Signed up")  # ✅ Add this
            return redirect('greet-user')
    return render(request, 'register.html')


# ==========================
# API Views (DRF)
# ==========================
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
        item, _ = InventoryItem.objects.get_or_create(player_id=id, itemId=data['itemId'])
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
