from django.shortcuts import render
from .models import Book, Offer
from .forms import OfferForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

def home(request):
    return render(request, 'books/home.html')

def offer_list(request):
    offers = Offer.objects.filter(active=True)
    return render(request, 'books/book_list.html', {'offers': offers})

def book_list(request):
    offers = Offer.objects.filter(active=True)
    return render(request, 'books/book_list.html', {'offers': offers})

@login_required
def my_offers(request):
    offers = Offer.objects.filter(seller=request.user)
    return render(request, 'books/my_offers.html', {'offers': offers})

@login_required
def create_offer_view(request):
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.seller = request.user
            offer.save()
            return redirect('thanks')
    else:
        form = OfferForm()
    return render(request, 'books/create_offer.html', {'form': form})

def thanks_view(request):
    return render(request, 'books/thanks.html')

def offer_detail(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    return render(request, 'books/offer_detail.html', {'offer': offer})