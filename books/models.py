from django.db import models
from django.contrib.auth.models import User

class SchoolBook(models.Model):
    """Offizielle Bücherliste der Europäischen Schule Karlsruhe"""
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=200, blank=True)
    isbn = models.CharField(max_length=20, unique=True)
    edition = models.CharField(max_length=50, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    school_class = models.CharField(max_length=20)  # S1DE, S2EN, etc.
    subject = models.CharField(max_length=100)
    section = models.CharField(max_length=50)  # DE, EN, FR
    notes = models.TextField(blank=True)
    academic_year = models.CharField(max_length=20, default="2023-2024")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['school_class', 'subject', 'title']
        indexes = [
            models.Index(fields=['school_class', 'subject']),
            models.Index(fields=['section']),
            models.Index(fields=['isbn']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.school_class} - {self.subject})"
    
    def get_section_display(self):
        section_map = {
            'DE': 'German Section',
            'EN': 'English Section', 
            'FR': 'French Section',
        }
        return section_map.get(self.section, self.section)

class StudentOffer(models.Model):
    """Angebote von Schülern für offizielle Schulbücher"""
    CONDITION_CHOICES = [
        ('new', 'Very good (like new)'),
        ('used', 'Normal use'),
        ('worn', 'Acceptable'),
        ('poor', 'Very used'),
    ]
    
    school_book = models.ForeignKey(SchoolBook, on_delete=models.CASCADE, related_name='offers')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_offers')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='book_offers/', blank=True)
    additional_notes = models.TextField(blank=True, help_text="Additional condition details, markings, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['school_book', 'is_active']),
            models.Index(fields=['seller', 'is_active']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.school_book.title} - €{self.price} by {self.seller.username}"

# Legacy models für Rückwärtskompatibilität
class Book(models.Model):
    """Legacy model - wird durch SchoolBook ersetzt"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    edition = models.CharField(max_length=50, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    section = models.CharField(max_length=50)
    school_class = models.CharField(max_length=10)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.school_class} {self.section})"

class Offer(models.Model):
    """Legacy model - wird durch StudentOffer ersetzt"""
    CONDITION_CHOICES = [
        ('new', 'Very good (like new)'),
        ('used', 'Normal use'),
        ('worn', 'Acceptable'),
        ('poor', 'Very used'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    contact_email = models.EmailField()
    image = models.ImageField(upload_to='book_images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.book.title} – {self.price}€ by {self.seller.username}"