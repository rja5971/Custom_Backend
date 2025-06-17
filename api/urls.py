from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, UserGreetingView

urlpatterns = [
    path('auth/register', views.RegisterView.as_view()),
    path('auth/login', TokenObtainPairView.as_view()),
    path('auth/token/refresh', TokenRefreshView.as_view()),
    path('server-time', views.ServerTimeView.as_view()),
    path('players/<int:id>/data', views.PlayerDataView.as_view()),
    path('players/<int:id>/inventory', views.InventoryView.as_view()),
    path('players/<int:id>/friends', views.FriendView.as_view()),
    path('players/<int:id>/assets', views.AssetUploadView.as_view()),
    path('greet/', UserGreetingView.as_view(), name='greet-user'),
]
