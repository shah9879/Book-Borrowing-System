from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from books.models import Book
from chat.models import Chat

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
    return redirect('login')  # Fixed typo: was "reidrect"

@login_required
def profile_view(request):
    # Get user's books
    my_books = Book.objects.filter(owner=request.user)
    
    # Get borrowed books
    borrowed_chats = Chat.objects.filter(
        participants=request.user
    ).exclude(book__owner=request.user)
    
    borrowed_books = [chat.book for chat in borrowed_chats]
    
    # Get books lent out (books owned but currently unavailable)
    lent_books = Book.objects.filter(owner=request.user, available=False)
    
    context = {
        'my_books': my_books,
        'borrowed_books': borrowed_books,
        'lent_books': lent_books,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile_edit.html', context)