from django import forms
from .models import Book, Offer

class OfferForm(forms.ModelForm):
    # Book fields
    book_title = forms.CharField(max_length=200, label="Book Title")
    book_author = forms.CharField(max_length=100, label="Author")
    book_isbn = forms.CharField(max_length=13, label="ISBN (optional)", required=False)
    book_edition = forms.CharField(max_length=50, label="Edition (optional)", required=False)
    book_publisher = forms.CharField(max_length=100, label="Publisher (optional)", required=False)
    book_section = forms.ChoiceField(
        choices=[
            ('EN', 'English'),
            ('DE', 'German'),
            ('FR', 'French'),
            ('MA', 'Mathematics'),
            ('SC', 'Sciences'),
            ('HI', 'History'),
            ('OTHER', 'Other'),
        ],
        label="Subject/Section"
    )
    book_school_class = forms.ChoiceField(
        choices=[
            ('S1', 'S1'),
            ('S2', 'S2'),
            ('S3', 'S3'),
            ('S4', 'S4'),
            ('S5', 'S5'),
            ('S6', 'S6'),
            ('S7', 'S7'),
        ],
        label="School Class"
    )
    book_notes = forms.CharField(
        widget=forms.Textarea(rows=3),
        label="Additional Notes (optional)",
        required=False
    )

    class Meta:
        model = Offer
        fields = ['condition', 'price', 'contact_email', 'image']
        widgets = {
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'condition': 'Book Condition',
            'price': 'Price (€)',
            'contact_email': 'Contact Email',
            'image': 'Book Photo (optional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # If editing existing offer, populate book fields
        if self.instance and self.instance.pk and self.instance.book:
            book = self.instance.book
            self.fields['book_title'].initial = book.title
            self.fields['book_author'].initial = book.author
            self.fields['book_isbn'].initial = book.isbn
            self.fields['book_edition'].initial = book.edition
            self.fields['book_publisher'].initial = book.publisher
            self.fields['book_section'].initial = book.section
            self.fields['book_school_class'].initial = book.school_class
            self.fields['book_notes'].initial = book.notes

    def save(self, commit=True):
        # Get or create the book
        book_data = {
            'title': self.cleaned_data['book_title'],
            'author': self.cleaned_data['book_author'],
            'isbn': self.cleaned_data.get('book_isbn', ''),
            'edition': self.cleaned_data.get('book_edition', ''),
            'publisher': self.cleaned_data.get('book_publisher', ''),
            'section': self.cleaned_data['book_section'],
            'school_class': self.cleaned_data['book_school_class'],
            'notes': self.cleaned_data.get('book_notes', ''),
        }
        
        # Try to find existing book by ISBN or create new one
        if book_data['isbn']:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
        else:
            # Create unique ISBN if none provided
            import uuid
            book_data['isbn'] = str(uuid.uuid4())[:13]
            book = Book.objects.create(**book_data)
        
        # Save the offer
        offer = super().save(commit=False)
        offer.book = book
        
        if commit:
            offer.save()
        
        return offer