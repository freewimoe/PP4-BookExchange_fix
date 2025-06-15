from django.urls import path
from . import views

urlpatterns = [
    path('', views.offer_list, name='offer_list'),  # das ist deine aktuelle View!
    path('offer/', views.create_offer_view, name='create_offer'),
    path('thanks/', views.thanks_view, name='thanks'),  # neue Route
    path('offers/<int:offer_id>/', views.offer_detail, name='offer_detail'),

]
