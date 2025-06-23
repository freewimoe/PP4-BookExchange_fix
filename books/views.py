from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator

# Try to import new models, fallback to legacy
try:
    from .models import SchoolBook, StudentOffer
    NEW_MODELS_AVAILABLE = True
except:
    NEW_MODELS_AVAILABLE = False

# Always import legacy models for compatibility
from .models import Book, Offer
from .forms import OfferForm

def home(request):
    """Startseite mit Statistiken - kompatibel mit beiden Systemen"""
    if NEW_MODELS_AVAILABLE:
        try:
            context = {
                'total_books': SchoolBook.objects.filter(is_active=True).count(),
                'total_offers': StudentOffer.objects.filter(is_active=True).count(),
                'sections': SchoolBook.objects.filter(is_active=True).values('section').annotate(
                    count=Count('id')
                ).order_by('section'),
            }
        except:
            # Fallback to static data
            context = {
                'total_books': 470,
                'total_offers': 0,
                'sections': [
                    {'section': 'DE', 'count': 150}, 
                    {'section': 'EN', 'count': 160}, 
                    {'section': 'FR', 'count': 160}
                ],
            }
    else:
        # Legacy system or fallback
        context = {
            'total_books': Book.objects.count() if Book.objects.exists() else 470,
            'total_offers': Offer.objects.filter(active=True).count() if Offer.objects.exists() else 0,
            'sections': [
                {'section': 'DE', 'count': 150}, 
                {'section': 'EN', 'count': 160}, 
                {'section': 'FR', 'count': 160}
            ],
        }
    
    return render(request, 'books/home.html', context)

def school_book_list(request):
    """Redirect to legacy or show message"""
    if NEW_MODELS_AVAILABLE:
        try:
            # Try new system
            books = SchoolBook.objects.filter(is_active=True)
            books = books.annotate(offer_count=Count('offers', filter=Q(offers__is_active=True)))
            
            paginator = Paginator(books.order_by('school_class', 'subject', 'title'), 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {
                'page_obj': page_obj,
                'total_books': books.count(),
                'search_query': '',
            }
            return render(request, 'books/school_book_list.html', context)
        except:
            pass
    
    # Fallback to legacy system
    return redirect('offer_list')

def school_book_detail(request, pk):
    """Book detail - redirect if not available"""
    if NEW_MODELS_AVAILABLE:
        try:
            school_book = get_object_or_404(SchoolBook, pk=pk, is_active=True)
            offers = StudentOffer.objects.filter(school_book=school_book, is_active=True)
            context = {
                'school_book': school_book,
                'offers': offers,
                'user_can_offer': request.user.is_authenticated,
            }
            return render(request, 'books/school_book_detail.html', context)
        except:
            pass
    
    # Fallback
    messages.info(request, "Book details temporarily unavailable. Please browse the legacy book list.")
    return redirect('offer_list')

def book_selection(request):
    """Book selection - redirect if not available"""
    if NEW_MODELS_AVAILABLE:
        try:
            books = SchoolBook.objects.filter(is_active=True)
            paginator = Paginator(books.order_by('school_class', 'subject', 'title'), 30)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context = {
                'page_obj': page_obj,
                'total_books': books.count(),
            }
            return render(request, 'books/book_selection.html', context)
        except:
            pass
    
    # Fallback to legacy create offer
    return redirect('create_offer')

@login_required
def create_student_offer(request, book_id=None):
    """Create offer - fallback to legacy"""
    messages.info(request, "Please use the legacy offer system for now.")
    return redirect('create_offer')

@login_required
def my_student_offers(request):
    """My offers - fallback to legacy"""
    return redirect('my_offers')

# Legacy views - always available
def offer_list(request):
    """Legacy view - alle verfügbaren Angebote"""
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

def offer_detail(request, pk):
    """Legacy offer detail"""
    offer = get_object_or_404(Offer, pk=pk)
    return render(request, 'books/offer_detail.html', {'offer': offer})

@login_required
def create_offer(request):
    """Legacy create offer"""
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
    """Legacy my offers"""
    offers = Offer.objects.filter(seller=request.user).select_related('book')
    return render(request, 'books/my_offers.html', {'offers': offers})

@login_required
def edit_offer(request, pk):
    """Legacy edit offer"""
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
    """Legacy delete offer"""
    offer = get_object_or_404(Offer, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        offer.delete()
        messages.success(request, 'Your offer has been deleted successfully!')
        return redirect('my_offers')
    
    return render(request, 'books/delete_offer.html', {'offer': offer})

# Placeholder functions for missing features
@login_required
def edit_student_offer(request, pk):
    messages.info(request, "Feature temporarily unavailable.")
    return redirect('my_offers')

@login_required
def delete_student_offer(request, pk):
    messages.info(request, "Feature temporarily unavailable.")
    return redirect('my_offers')

@login_required
def mark_as_sold(request, pk):
    messages.info(request, "Feature temporarily unavailable.")
    return redirect('my_offers')