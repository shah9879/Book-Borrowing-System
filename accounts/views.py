from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save city to profile
            user.profile.city = form.cleaned_data.get('city')
            user.profile.save()
            messages.success(request, 'Account created successfully! You can now log in')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('browse_books')
		else:
			messages.error(request, 'Invalid username or password')
	return render(request, 'accounts/login.html')

def logout_view(request):
	logout(request)
	return reidrect('login')