from django.contrib import admin
from django.urls import path, include  # <- NEU hinzugefügt
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),  # <- NEU: leitet die Startseite an deine App weiter    # deine URLs
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


