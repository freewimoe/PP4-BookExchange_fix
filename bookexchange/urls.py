from django.contrib import admin
from django.urls import path, include  # <- NEU hinzugefügt
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from books import views as book_views  # <- Importiere deine Views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', book_views.home, name='home'),
    path('', include('books.urls')),  # <- NEU: leitet die Startseite an deine App weiter    # deine URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='book_list'), name='logout'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


