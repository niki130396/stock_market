from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.


class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/visualisations')
        return HttpResponseRedirect('/accounts/register')


class RegistrationView(View):
    def get(self, request):
        return render(request, 'registration/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        duplicate_email = User.objects.get(email=email)
        if not duplicate_email:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
                )
            return HttpResponseRedirect('/visualisations')
        else:
            return HttpResponseRedirect('/accounts/sign-up')