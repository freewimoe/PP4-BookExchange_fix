from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.offer_list, name='offer_list'),  # das ist deine aktuelle View!
    path('offer/', views.create_offer_view, name='create_offer'),
    path('thanks/', views.thanks_view, name='thanks'),  # neue Route
    path('offers/<int:offer_id>/', views.offer_detail, name='offer_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='books/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='offer_list'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='books/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='books/password_change_done.html'), name='password_change_done'),
    path('books/', views.book_list, name='book_list'),
    path('admin/', admin.site.urls),
    path('', include('books.urls')),  # 🔥 ganz wichtig!
    path('accounts/', include('django.contrib.auth.urls')),  # für Login, Logout, Passwort ändern
    path('accounts/signup/', views.signup, name='signup'),  # für die Registrierung

]
