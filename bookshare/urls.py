from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import redirect
urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', include('books.urls')), 
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),  # ← Add this
    path('', lambda request: redirect('browse_books')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)