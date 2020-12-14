from django.urls import path, include
from accounts import views
import allauth

urlpatterns = [
    path('sign-up/', views.LoginView.as_view(), name='sign-up'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('profile/', views.ProfileInfo.as_view(), name='profile'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('premium/', views.GoPremiumView.as_view(), name='premium'),
    path('', include('allauth.urls'))
]
