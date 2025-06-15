from django.shortcuts import render, redirect
from .models import Book
from .forms import OfferForm

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def create_offer_view(request):
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('thanks')  # nach erfolgreicher Speicherung
    else:
        form = OfferForm()
    return render(request, 'books/create_offer.html', {'form': form})


def offer_list(request):
    offers = Offer.objects.filter(active=True).order_by('-created_at')
    return render(request, 'books/offer_list.html', {'offers': offers})


