from django import forms
from django.db.models import Q
from .models import SchoolBook, StudentOffer, Book, Offer

class BookSearchForm(forms.Form):
    """Formular für die Buchsuche"""
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, author, or subject...',
        })
    )
    
    section = forms.ChoiceField(
        choices=[('', 'All Sections')] + [
            ('DE', 'German Section'),
            ('EN', 'English Section'),
            ('FR', 'French Section'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    school_class = forms.ChoiceField(
        choices=[('', 'All Classes')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    subject = forms.ChoiceField(
        choices=[('', 'All Subjects')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically populate choices from database
        active_books = SchoolBook.objects.filter(is_active=True)
        
        # School classes
        classes = active_books.values_list('school_class', flat=True).distinct().order_by('school_class')
        self.fields['school_class'].choices = [('', 'All Classes')] + [(c, c) for c in classes if c]
        
        # Subjects
        subjects = active_books.values_list('subject', flat=True).distinct().order_by('subject')
        self.fields['subject'].choices = [('', 'All Subjects')] + [(s, s) for s in subjects if s]

class StudentOfferForm(forms.ModelForm):
    """Formular für Schüler-Angebote basierend auf offizieller Bücherliste"""
    
    class Meta:
        model = StudentOffer
        fields = ['school_book', 'condition', 'price', 'contact_email', 'contact_phone', 'image', 'additional_notes']
        
        widgets = {
            'school_book': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any additional notes about condition, markings, etc.'}),
        }
        
        labels = {
            'school_book': 'Select Book from Official List',
            'condition': 'Book Condition',
            'price': 'Price (€)',
            'contact_email': 'Contact Email',
            'contact_phone': 'Contact Phone (optional)',
            'image': 'Book Photo (optional)',
            'additional_notes': 'Additional Notes (optional)',
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        initial_book = kwargs.pop('initial_book', None)
        super().__init__(*args, **kwargs)
        
        # Only show active books
        self.fields['school_book'].queryset = SchoolBook.objects.filter(is_active=True).order_by('school_class', 'subject', 'title')
        
        # Set initial book if provided
        if initial_book:
            self.fields['school_book'].initial = initial_book
        
        # Pre-fill contact email if user is logged in
        if user and user.is_authenticated:
            self.fields['contact_email'].initial = user.email

class BookSelectionForm(forms.Form):
    """Formular zur Buchauswahl mit Filtern"""
    
    section = forms.ChoiceField(
        choices=[('', 'All Sections')] + [
            ('DE', 'German Section'),
            ('EN', 'English Section'),
            ('FR', 'French Section'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    school_class = forms.ChoiceField(
        choices=[('', 'All Classes')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    subject = forms.ChoiceField(
        choices=[('', 'All Subjects')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate choices
        active_books = SchoolBook.objects.filter(is_active=True)
        
        classes = active_books.values_list('school_class', flat=True).distinct().order_by('school_class')
        self.fields['school_class'].choices = [('', 'All Classes')] + [(c, c) for c in classes if c]
        
        subjects = active_books.values_list('subject', flat=True).distinct().order_by('subject')
        self.fields['subject'].choices = [('', 'All Subjects')] + [(s, s) for s in subjects if s]

# Legacy forms für Rückwärtskompatibilität
class OfferForm(forms.ModelForm):
    """Legacy form - wird durch StudentOfferForm ersetzt"""
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
        widget=forms.Textarea(attrs={'rows': 3}),
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