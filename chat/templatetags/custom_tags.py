from django import template
from chat.models import Message

register = template.Library()

@register.simple_tag
def unread_message_count(user):
    """
    Counts unread messages for a user across all their chats
    """
    # Count messages that:
    # - Are NOT sent by the user (exclude sender=user)
    # - Are NOT read (is_read=False)
    # - Are in chats where user is a participant
    
    from chat.models import Chat
    
    # Get all chats where user is involved
    user_chats = Chat.objects.filter(participants=user)
    
    # Count unread messages in those chats (not sent by this user)
    unread = Message.objects.filter(
        chat__in=user_chats,
        is_read=False
    ).exclude(sender=user).count()
    
    return unread