from django.shortcuts import render
from django.views.generic import View, RedirectView
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from accounts.models import StockMarketUser
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
            return HttpResponseRedirect('/accounts/profile')
        return HttpResponseRedirect('/accounts/register')


class RegistrationView(View):
    def get(self, request):
        return render(request, 'registration/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email)
        if not user:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
                )
            user = User.objects.get(email=email)
            login(request, user)
            return HttpResponseRedirect('/visualisations')
        return HttpResponseRedirect('/accounts/sign-up')


class ProfileInfo(LoginRequiredMixin, View):
    login_url = '/accounts/sign-up'

    def get(self, request):
        user_context = {
            'username': request.user.username,
            'email': request.user.email
        }
        return render(request, 'profile.html', context=user_context)


class LogoutView(LoginRequiredMixin, RedirectView):
    login_url = 'accounts/sign-up'
    permanent = False
    query_string = True
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class GoPremiumView(LoginRequiredMixin, RedirectView):
    login_url = 'accounts/sign-up'
    permanent = False
    query_string = True
    pattern_name = 'stock_prices'

    def get_redirect_url(self, *args, **kwargs):
        user = StockMarketUser.objects.get(user__username=self.request.user.username)
        user.account_type = 2
        user.save()
        return super(GoPremiumView, self).get_redirect_url(*args, **kwargs)


"""
from django.contrib.auth.models import User
user = User.objects.get(username='ivan.ivanov')
"""


"""
from accounts.models import StockMarketUser
username = 'ivan.ivanov'
user = StockMarketUser.objects.get(user__username=username)
"""