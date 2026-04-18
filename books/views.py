from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, BorrowRequest
from chat.models import Chat, Message  # Add this import at top
from django.contrib import messages
from .forms import BookForm
# Create your views here.


@login_required  # Add this decorator!
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)  # Added request.FILES for images
        if form.is_valid():
            book = form.save(commit=False)  # Don't save yet
            book.owner = request.user        # Set the owner!
            book.save()                      # Now save
            messages.success(request, 'Book added successfully!')
            return redirect('browse_books')  # Changed from 'book_list'
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})


@login_required
def browse_books(request):
    # Get the selected city from URL parameter (?city=Lahore)
    selected_city = request.GET.get('city', 'all')
    
    # Start with all available books
    books = Book.objects.filter(available=True)
    
    # If a specific city is selected, filter by that city
    if selected_city != 'all':
        books = books.filter(city=selected_city)
    
    # Order by newest first
    books = books.order_by('-created_at')
    
    # Get list of all unique cities for the dropdown
    all_cities = Book.objects.values_list('city', flat=True).distinct().order_by('city')
    
    context = {
        'books': books,
        'all_cities': all_cities,
        'selected_city': selected_city,
    }
    return render(request, 'books/browse_books.html', context)


@login_required
def my_books(request):
    books = Book.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'books/my_books.html', {'books':books})

@login_required
def request_borrow(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if book.owner == request.user:
        messages.warning(request, "You cannot request your own book.")
        return redirect('browse_books')
    
    # Check if chat already exists for this book between these users
    existing_chat = Chat.objects.filter(
        book=book,
        participants=request.user
    ).filter(participants=book.owner).first()
    
    if existing_chat:
        messages.info(request, "Conversation already exists for this book.")
        return redirect('chat_detail', chat_id=existing_chat.id)
    
    # Create new chat
    chat = Chat.objects.create(book=book)
    chat.participants.add(request.user, book.owner)
    
    # Create initial message
    Message.objects.create(
        chat=chat,
        sender=request.user,
        content=f"Hi! I'm interested in borrowing '{book.title}'."
    )
    
    messages.success(request, "Chat started with book owner!")
    return redirect('chat_detail', chat_id=chat.id)

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    #Check if user already requested this book
    existing_request = BorrowRequest.objects.filter(
        book=book,
        borrower=request.user,
        status='Pending'
        ).first()

    context={
        'book':book,
        'existing_request':existing_request,
    }
    return render(request, 'books/book_detail.html', context)


@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Security: Only owner can edit
    if book.owner != request.user:
        messages.error(request, "You can only edit your own books!")
        return redirect('browse_books')
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect('my_books')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Security: Only owner can delete
    if book.owner != request.user:
        messages.error(request, "You can only delete your own books!")
        return redirect('browse_books')
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f"'{book_title}' has been deleted.")
        return redirect('my_books')
    
    return render(request, 'books/delete_book.html', {'book': book})

@login_required
def borrowed_books(request):
    # Get all chats where user is the borrower (not the owner)
    from chat.models import Chat
    
    borrowed_chats = Chat.objects.filter(
        participants=request.user
    ).exclude(book__owner=request.user)
    
    # Create list of borrowed books with chat info
    borrowed_list = []
    for chat in borrowed_chats:
        borrowed_list.append({
            'book': chat.book,
            'owner': chat.book.owner,
            'chat': chat,
        })
    
    return render(request, 'books/borrowed_books.html', {'borrowed_list': borrowed_list})

@login_required
def return_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # Mark book as available again
    book.available = True
    book.save()
    
    messages.success(request, f"'{book.title}' has been marked as returned!")
    
    # Redirect based on who's returning (owner or borrower)
    if book.owner == request.user:
        return redirect('my_books')
    else:
        return redirect('borrowed_books')