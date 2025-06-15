from django import forms
from .models import Offer

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['book', 'condition', 'price', 'contact_email', 'image']

        widgets = {
            'book': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'book': 'Book from list',
            'condition': 'Condition of your copy',
            'price': 'Selling Price (EUR)',
            'contact_email': 'Your Email for Contact',
            'image': 'Photo of the book (optional)',
        }
