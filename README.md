## 💡 Usage Guide

### For Book Owners

1. **Add a Book**
   - Click "➕ Add Book" in the navigation
   - Fill in book details (title, author, ISBN, description, city)
   - Upload a cover image or provide an image URL
   - Select delivery options (Pickup/Delivery/Both)
   - Submit to list your book

2. **Manage Your Books**
   - View your books in "📚 My Books"
   - Edit book details anytime
   - Delete books you no longer want to share
   - See which books are currently lent out

3. **Handle Borrow Requests**
   - Receive messages when someone requests your book
   - Discuss pickup/delivery details in chat
   - Click "✅ Confirm Borrowing" to mark book as lent
   - Click "↩️ Mark as Returned" when book is returned

### For Borrowers

1. **Find Books**
   - Browse all available books
   - Filter by city to find nearby books
   - Click on books to view full details

2. **Request a Book**
   - Click "💬 Request" on any available book
   - Chat opens automatically with the owner
   - Discuss pickup location, time, and delivery options
   - Wait for owner to confirm borrowing

3. **Track Your Borrowed Books**
   - View borrowed books in "📖 Borrowed Books"
   - Message the owner anytime
   - Coordinate return details through chat

## 🔧 Configuration

### Media Files Setup

In `settings.py`, ensure these settings are configured:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

In main `urls.py`, add media file serving:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your url patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 🎨 Customization

### Changing Color Scheme

The primary color is green (`#4CAF50`). To change it:
- Edit `templates/base.html` header background
- Update button colors in individual templates
- Modify badge colors throughout the application

### Adding More Features

Consider adding:
- Email notifications for new messages
- Search functionality (by title, author, ISBN)
- Book categories/genres
- User ratings and reviews
- Due date tracking
- Book condition reporting
- Multi-language support

## 🐛 Troubleshooting

### Images not displaying
- Ensure `MEDIA_ROOT` is set correctly in `settings.py`
- Check that media URLs are configured in `urls.py`
- Verify file permissions on the `media/` directory

### Template not found errors
- Check template file names match exactly (case-sensitive)
- Verify template directory structure
- Ensure app is in `INSTALLED_APPS` in `settings.py`

### Database errors
- Run migrations: `python manage.py migrate`
- If persistent, delete `db.sqlite3` and run migrations again

## 📝 Models Overview

### Book Model
- `owner`: ForeignKey to User
- `title`, `author`, `isbn`, `description`
- `city`: Location of the book
- `cover_image`: Uploaded image file
- `cover_url`: Alternative image URL
- `delivery_option`: Pickup/Delivery/Both
- `available`: Boolean status

### Profile Model
- `user`: OneToOneField to User
- `city`: User's city

### Chat Model
- `participants`: ManyToMany to User
- `book`: ForeignKey to Book
- `last_updated`: Auto-updated timestamp

### Message Model
- `chat`: ForeignKey to Chat
- `sender`: ForeignKey to User
- `content`: Message text
- `timestamp`: When sent
- `is_read`: Read status

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

Created with ❤️ by [Your Name]

## 🙏 Acknowledgments

- Built with Django framework
- Icons: Unicode emoji characters
- Inspired by community book-sharing initiatives

## 📞 Contact

For questions or support, please open an issue on GitHub or contact [your-email@example.com]

---

**Happy Book Sharing! 📚✨**
