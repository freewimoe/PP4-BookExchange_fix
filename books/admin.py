from django.contrib import admin
from .models import Book, Offer, SchoolBook, StudentOffer

# Legacy models
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'school_class', 'section']
    list_filter = ['school_class', 'section']
    search_fields = ['title', 'author', 'isbn']

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['book', 'seller', 'condition', 'price', 'created_at']
    list_filter = ['condition', 'created_at']
    search_fields = ['book__title', 'seller__username']

# New models für Schulbücher
@admin.register(SchoolBook)
class SchoolBookAdmin(admin.ModelAdmin):
    list_display = ['title', 'school_class', 'subject', 'section', 'publisher', 'is_active']
    list_filter = ['school_class', 'subject', 'section', 'is_active', 'academic_year']
    search_fields = ['title', 'author', 'isbn', 'subject']
    ordering = ['school_class', 'subject', 'title']
    
    # Bessere Darstellung
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'isbn', 'edition', 'publisher')
        }),
        ('School Information', {
            'fields': ('school_class', 'subject', 'section', 'academic_year')
        }),
        ('Additional', {
            'fields': ('notes', 'is_active')
        }),
    )

@admin.register(StudentOffer)
class StudentOfferAdmin(admin.ModelAdmin):
    list_display = ['school_book', 'seller', 'condition', 'price', 'is_active', 'is_sold', 'created_at']
    list_filter = ['condition', 'is_active', 'is_sold', 'created_at', 'school_book__section']
    search_fields = ['school_book__title', 'seller__username', 'contact_email']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Offer Details', {
            'fields': ('school_book', 'seller', 'condition', 'price')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Additional Information', {
            'fields': ('image', 'additional_notes', 'is_active', 'is_sold')
        }),
    )