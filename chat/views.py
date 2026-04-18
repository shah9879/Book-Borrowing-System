from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages as django_messages
from .models import Chat, Message
from django.db.models import Q, Max
# Create your views here.

@login_required
def chat_list(request):
    # Get all chats where YOU are a participant
    chats = Chat.objects.filter(
        participants=request.user
    ).annotate(                                       # "annotate" adds extra calculated data
        last_message_time=Max('messages__timestamp')  # Find latest message time
    ).order_by('-last_message_time')                  # Show newest chats first
    
    # For each chat, calculate useful info
    chat_data = []
    for chat in chats:
        # Count unread messages (not sent by you, not read yet)
        unread_count = Message.objects.filter(
            chat=chat,
            is_read=False                             # Not read
        ).exclude(sender=request.user).count()        # Don't count your own messages
        
        # Get the last message to show preview
        last_message = chat.messages.order_by('-timestamp').first()
        
        # Get the OTHER person in the chat (not you)
        other_user = chat.participants.exclude(id=request.user.id).first()
        
        # Save all this info
        chat_data.append({
            'chat': chat,
            'unread_count': unread_count,  # For notification badge
            'last_message': last_message,  # Show preview
            'other_user': other_user,      # Show who you're talking to
        })
    
    return render(request, 'chat/chat_list.html', {'chat_data': chat_data})

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    
    # Check if user is participant
    if request.user not in chat.participants.all():
        django_messages.error(request, "You don't have access to this chat.")
        return redirect('chat_list')
    
    # Mark messages as read
    Message.objects.filter(
        chat=chat,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    # Handle confirming borrowing (owner confirms)
    if request.method == 'POST' and 'confirm_borrow' in request.POST:
        if chat.book.owner == request.user and chat.book.available:
            chat.book.available = False
            chat.book.save()
            
            # Send system message
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=f"✅ Borrowing confirmed! {chat.book.title} is now marked as borrowed."
            )
            django_messages.success(request, "Book marked as borrowed!")
            return redirect('chat_detail', chat_id=chat_id)
    
    # Handle new message
    if request.method == 'POST' and 'content' in request.POST:
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=content
            )
            return redirect('chat_detail', chat_id=chat_id)
    
    messages_list = chat.messages.order_by('timestamp')
    other_user = chat.participants.exclude(id=request.user.id).first()
    
    # Check if current user is the owner
    is_owner = chat.book.owner == request.user
    
    context = {
        'chat': chat,
        'messages': messages_list,
        'other_user': other_user,
        'is_owner': is_owner,
    }
    return render(request, 'chat/chat_detail.html', context)