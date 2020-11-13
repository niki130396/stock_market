from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect

# Create your views here.


class LoginView(View):
    def get(self, request):
        return render(request, 'registration/test_login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/visualisations')
