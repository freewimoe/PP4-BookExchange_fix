from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Book, Offer
from .forms import OfferForm

def home(request):
    """Startseite"""
    return render(request, 'books/home.html')

def offer_list(request):
    """Alle aktiven Angebote anzeigen"""
    offers = Offer.objects.filter(active=True).select_related('book', 'seller')
    
    # Such-Funktionalität
    search_query = request.GET.get('search')
    if search_query:
        offers = offers.filter(
            Q(book__title__icontains=search_query) |
            Q(book__author__icontains=search_query) |
            Q(book__section__icontains=search_query) |
            Q(book__school_class__icontains=search_query)
        )
    
    context = {
        'offers': offers,
        'search_query': search_query,
    }
    return render(request, 'books/offer_list.html', context)

@login_required
def create_offer(request):
    """Neues Angebot erstellen"""
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.seller = request.user
            offer.save()
            messages.success(request, 'Your book offer has been created successfully!')
            return redirect('offer_detail', pk=offer.pk)
    else:
        form = OfferForm()
    
    return render(request, 'books/create_offer.html', {'form': form})

@login_required
def my_offers(request):
    """Meine Angebote anzeigen"""
    offers = Offer.objects.filter(seller=request.user).select_related('book')
    return render(request, 'books/my_offers.html', {'offers': offers})

def offer_detail(request, pk):
    """Details eines Angebots anzeigen"""
    offer = get_object_or_404(Offer, pk=pk)
    return render(request, 'books/offer_detail.html', {'offer': offer})

@login_required
def edit_offer(request, pk):
    """Angebot bearbeiten"""
    offer = get_object_or_404(Offer, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your offer has been updated successfully!')
            return redirect('offer_detail', pk=offer.pk)
    else:
        form = OfferForm(instance=offer)
    
    return render(request, 'books/edit_offer.html', {'form': form, 'offer': offer})

@login_required
def delete_offer(request, pk):
    """Angebot löschen"""
    offer = get_object_or_404(Offer, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        offer.delete()
        messages.success(request, 'Your offer has been deleted successfully!')
        return redirect('my_offers')
    
    return render(request, 'books/delete_offer.html', {'offer': offer})