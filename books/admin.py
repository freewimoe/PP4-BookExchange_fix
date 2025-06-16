from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Offer, Book

class BookAdmin(ImportExportModelAdmin):
    pass
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
admin.site.register(Book, BookAdmin)