from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import SignUpForm, ProfileForm
from django.urls import reverse

# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# Forms and models
from .models import Profile
from .forms import SignUpForm, ProfileForm

# Messages
from django.contrib import messages

# Create your views here.

def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!!')
            return HttpResponseRedirect(reverse('login_app:login'))
    return render(request, 'login_app/sign_up.html', {'form': form})

def login_user(request):
    form = AuthenticationForm()
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('shop_app:home'))
    return render(request, 'login_app/login.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, 'You are logged out!!')
    return HttpResponseRedirect(reverse('shop_app:home'))

@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)

    form = ProfileForm(instance=profile)
    if request.method=='POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes saved!!')
            form = ProfileForm(instance=profile)
    return render(request, 'login_app/change_profile.html', {'form': form}) 