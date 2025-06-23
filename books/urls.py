from django.urls import path
from . import views

urlpatterns = [
    # Startseite 
    path('', views.home, name='home'),
    
    # Alle Angebote anzeigen (Browse Books)
    path('offers/', views.offer_list, name='offer_list'),
    
    # Neues Angebot erstellen
    path('offers/create/', views.create_offer, name='create_offer'),
    
    # Meine Angebote anzeigen
    path('offers/my/', views.my_offers, name='my_offers'),
    
    # Angebot details anzeigen
    path('offers/<int:pk>/', views.offer_detail, name='offer_detail'),
    
    # Angebot bearbeiten
    path('offers/<int:pk>/edit/', views.edit_offer, name='edit_offer'),
    
    # Angebot löschen
    path('offers/<int:pk>/delete/', views.delete_offer, name='delete_offer'),
]