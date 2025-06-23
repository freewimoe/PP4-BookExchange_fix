from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Startseite 
    path('', views.home, name='home'),
    
    # Neue Schulbuch-URLs
    path('books/', views.school_book_list, name='school_book_list'),
    path('books/<int:pk>/', views.school_book_detail, name='school_book_detail'),
    path('books/<int:book_id>/offer/', views.create_student_offer, name='create_student_offer'),
    path('book-selection/', views.book_selection, name='book_selection'),
    
    # Student Offers
    path('offers/create/', views.create_student_offer, name='create_student_offer'),
    path('offers/my/', views.my_student_offers, name='my_student_offers'),
    path('offers/<int:pk>/edit/', views.edit_student_offer, name='edit_student_offer'),
    path('offers/<int:pk>/delete/', views.delete_student_offer, name='delete_student_offer'),
    path('offers/<int:pk>/sold/', views.mark_as_sold, name='mark_as_sold'),
    
    # Legacy URLs (für Rückwärtskompatibilität)
    path('offers/', views.offer_list, name='offer_list'),  # -> redirects to school_book_list
    path('legacy-offers/<int:pk>/', views.offer_detail, name='offer_detail'),
    path('legacy-create/', views.create_offer, name='create_offer'),  # -> redirects to book_selection
    path('legacy-my/', views.my_offers, name='my_offers'),  # -> redirects to my_student_offers
    path('legacy-edit/<int:pk>/', views.edit_offer, name='edit_offer'),
    path('legacy-delete/<int:pk>/', views.delete_offer, name='delete_offer'),
    
    # Auth URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]