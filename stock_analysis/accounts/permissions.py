from accounts.models import StockMarketUser
from django.http import HttpResponse


def is_premium(function):
    def wrapper(*args, **kwargs):
        request = args[1]
        user = StockMarketUser.objects.get(user__username=request.user.username)
        if user.account_type == 1:
            return HttpResponse('USER IS NOT PREMIUM')
        return function(*args, **kwargs)
    return wrapper
