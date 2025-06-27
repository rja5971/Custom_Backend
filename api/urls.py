from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView

urlpatterns = [
    # JWT API routes
    path('auth/register-api/', views.RegisterView.as_view(), name='register_api'),
    path('auth/login-api/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/logout-api/', views.LogoutAPIView.as_view(), name='logout_api'),

    # Game API routes
    path('server-time/', views.ServerTimeView.as_view()),
    path('players/<int:id>/data/', views.PlayerDataView.as_view()),
    path('players/<int:id>/inventory/', views.InventoryView.as_view()),
    path('players/<int:id>/friends/', views.FriendView.as_view()),
    path('players/<int:id>/assets/', views.AssetUploadView.as_view()),
    path('greet/', views.UserGreetingTemplateView.as_view(), name='greet-user'),

    # HTML form pages
    path('auth/login/', views.login_user, name='login_user'),
    path('auth/register/', views.register_user, name='register_user'),
    path('logout/', views.logout_view, name='logout'),
]
