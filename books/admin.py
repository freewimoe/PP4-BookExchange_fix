from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Book, Offer


# 📘 CSV-Import/Export-Resource für Book
class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        import_id_fields = ['isbn']  # für eindeutigen Import
        fields = (
            'title', 'author', 'isbn', 'edition',
            'publisher', 'section', 'school_class', 'notes'
        )


@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResource
    list_display = ('title', 'author', 'isbn', 'edition', 'school_class', 'section')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('school_class', 'section')


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'book', 'seller', 'condition', 'price',
        'contact_email', 'created_at', 'active',
    )
    list_filter = ('active', 'condition')
    search_fields = ('book__title', 'seller__username', 'contact_email')
