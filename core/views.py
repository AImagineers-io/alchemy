from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from urllib.parse import urlencode
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            message = urlencode({'message': 'Registration successful. Please log in with your new account.'})
            return redirect(f"{redirect('core:login').url}?{message}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def redirect_to_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    return redirect('core:login')
