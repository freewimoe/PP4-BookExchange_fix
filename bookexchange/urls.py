from django.contrib import admin
from django.urls import path, include  # <- NEU hinzugefügt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),  # <- NEU: leitet die Startseite an deine App weiter
]
