from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    
    # Both URL and file upload for cover image
    cover_url = models.URLField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    
    delivery_option = models.CharField(
        max_length=20,
        choices=[
            ('pickup', 'Pickup'),
            ('delivery', 'Delivery'),
            ('both', 'Both'),
        ],
        default='both'
    )
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_cover(self):
        """Return cover image or URL, whichever is available"""
        if self.cover_image:
            return self.cover_image.url
        return self.cover_url
    
    def __str__(self):
        return f"{self.title} by {self.author}"
        
        
class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_requests')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrow_requests')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests', null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.borrower.username} → {self.book.title} ({self.status})"

