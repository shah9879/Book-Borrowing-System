from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username
    
    def books_owned_count(self):
        return self.user.books.count()
    
    def books_borrowed_count(self):
        from chat.models import Chat
        return Chat.objects.filter(
            participants=self.user
        ).exclude(book__owner=self.user).count()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()