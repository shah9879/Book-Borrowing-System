from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_book, name='add_book'),
    path('browse/', views.browse_books, name='browse_books'),
    path('my/', views.my_books, name='my_books'), 
    path('request/<int:book_id>/', views.request_borrow, name='request_borrow'),
    path('detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('borrowed/', views.borrowed_books, name='borrowed_books'),  # ← ADD THIS
    path('return/<int:book_id>/', views.return_book, name='return_book'),  # ← ADD THIS
]