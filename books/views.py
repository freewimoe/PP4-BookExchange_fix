from django.shortcuts import render
from .models import Offer
from .forms import OfferForm

def offer_list(request):
    offers = Offer.objects.filter(active=True)
    return render(request, 'books/book_list.html', {'offers': offers})

def create_offer_view(request):
    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
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
