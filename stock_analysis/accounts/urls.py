from django.urls import path
from accounts import views


urlpatterns = [
    path('sign-up/', views.LoginView.as_view(), name='sign-up'),
]