from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    edition = models.CharField(max_length=50, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    section = models.CharField(max_length=50)  # EN, DE, FR
    school_class = models.CharField(max_length=10)  # S1–S7
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.school_class} {self.section})"

class Offer(models.Model):
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

