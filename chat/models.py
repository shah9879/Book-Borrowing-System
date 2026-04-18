from django.db import models
from django.contrib.auth.models import User
from books.models import Book
# Create your models here.

class Chat(models.Model):
	participants = models.ManyToManyField(User)
	book = models.ForeignKey(Book, on_delete = models.CASCADE, related_name = 'chats')
	last_updated = models.DateTimeField(auto_now = True)

	def __str__(self):
		return f"Chat about {self.book.title}"

class Message(models.Model):
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	is_read = models.BooleanField(default=False)

	def __str__(self):
		return f"From {self.sender.username} at {self.timestamp:%Y-%m-%d %H:%M}"