from django.contrib import admin
from .models import Offer

class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'book',           # das ForeignKey-Feld zeigt automatisch book.title im Admin
        'seller',         # verlinkt auf den Benutzer
        'condition',
        'price',
        'contact_email',
        'created_at',
        'active'
    )

admin.site.register(Offer, OfferAdmin)