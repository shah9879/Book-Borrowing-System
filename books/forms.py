from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'description', 'city', 'cover_image', 'cover_url', 'delivery_option']
        
        # Add help text to guide users
        help_texts = {
            'cover_image': 'Upload a book cover image from your computer',
            'cover_url': 'OR paste an image URL (if you don\'t upload a file)',
        }
        
        # Make both image fields optional (user can choose one)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
            'title': forms.TextInput(attrs={'size': 50}),
            'author': forms.TextInput(attrs={'size': 50}),
            'isbn': forms.TextInput(attrs={'size': 20}),
            'city': forms.TextInput(attrs={'size': 30}),
        }