# login_reg
from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    context = {
        'users':User.objects.all()
    }
    return render(request, 'login_reg/index.html', context)


def login(request):
    if request.method == "POST":
        verify = User.userManager.login(request.POST)

        if verify[0] == False:
            for alert in verify[1]:
                messages.add_message(request, messages.INFO, alert)
            return redirect(reverse('login_reg:index'))

        elif verify[0] == True:
            request.session['success'] = verify[1]
            request.session['thisUser'] = verify[2]
            return redirect(reverse('wishlist:index'))

        else:
            request.session.clear()
            return redirect(reverse('login_reg:index'))


def register(request):
    if request.method == "POST":
        verify = User.userManager.register(request.POST)

        if verify[0] == False:
            for alert in verify[1]:
                messages.add_message(request, messages.INFO, alert)
            return redirect(reverse('login_reg:index'))

        elif verify[0] == True:
            request.session['success'] = verify[1]
            request.session['thisUser'] = verify[2]
            return redirect(reverse('wishlist:index'))
        else:
            request.session.clear()
            return redirect(reverse('login_reg:index'))


def logout(request):
    request.session.clear()
    return redirect(reverse('login_reg:index'))
