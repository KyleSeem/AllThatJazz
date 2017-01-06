from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, Item, Wishlist

# Create your views here.
def index(request):
    id = request.session['thisUser']
    print(id)
    context = {
        'users':User.objects.all(),
        'thisUser':User.objects.get(id=id),
        'items':Item.objects.all(),
        'wishlists':Wishlist.objects.all(),
    }
    return render(request, 'wishlist/index.html', context)


def getItem(request, id):
    if request.method == "GET":
        print (id)
        context = {
            'users':User.objects.all(),
            'item':Item.objects.get(id=id),
            'wishlists':Wishlist.objects.all(),
        }
        return render(request, 'wishlist/getItem.html', context)

def add(request):
    if request.method == "GET":
        # Item.objects.all().delete()
        id = request.session['thisUser']
        context = {
            'thisUser':User.objects.get(id=id),
            'items':Item.objects.all(),
        }
        return render(request, 'wishlist/addItems.html', context)

    elif request.method == "POST":
        verify = Item.itemManager.create(request.POST)

        if verify[0] == False:
            for alert in verify[1]:
                messages.add_message(request, messages.INFO, alert)
            return redirect(reverse('wishlist:add'))

        elif verify[0] == True:
            thisUser = request.session['thisUser']
            note = verify[1]
            print(note)
            return redirect(reverse('wishlist:index'))

def addThis(request):
    if request.method == "POST":
        bridge = Item.itemManager.bridge_connections(request.POST)
        if bridge == True:
            print ('your wishlist updated')
            return redirect(reverse('wishlist:index'))
        else:
            print('ERROR')
            return HttpResponse('Whoops! Something went wrong! Please try again later.')

def delete(request):
    # delete entire existance of item
    if request.method == "POST":
        destroy = Item.itemManager.delete(request.POST)
        if destroy == True:
            return redirect(reverse('wishlist:index'))

def remove(request):
    # remove from user's wishlist only
    if request.method == "POST":
        extract = Item.itemManager.remove(request.POST)
        if extract == True:
            return redirect(reverse('wishlist:index'))
