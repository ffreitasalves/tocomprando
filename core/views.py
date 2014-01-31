from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login as authlogin, authenticate

def index(request):
    return render_to_response(
        'index.html',
        locals(),
        context_instance = RequestContext(request),
    )

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        new_user = User.objects.create_user(email,email,password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        user = authenticate(username=email, password=password)
        authlogin(request, user)

        return HttpResponseRedirect(reverse('home'))

    return render_to_response(
        'index.html',
        locals(),
        context_instance = RequestContext(request),
    )

def login(request):
    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            authlogin(request, user)
            return HttpResponseRedirect(reverse('home'))