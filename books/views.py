from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import SchoolBook, StudentOffer, Book, Offer  # Keep legacy for compatibility
from .forms import StudentOfferForm, BookSearchForm, BookSelectionForm

def home(request):
    """Startseite mit Statistiken"""
    context = {
        'total_books': SchoolBook.objects.filter(is_active=True).count(),
        'total_offers': StudentOffer.objects.filter(is_active=True).count(),
        'sections': SchoolBook.objects.filter(is_active=True).values('section').annotate(
            count=Count('id')
        ).order_by('section'),
    }
    return render(request, 'books/home.html', context)

def school_book_list(request):
    """Alle verfügbaren Schulbücher anzeigen mit Filtern"""
    # Get all active school books
    books = SchoolBook.objects.filter(is_active=True)
    
    # Search functionality
    search_form = BookSearchForm(request.GET)
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search')
        section = search_form.cleaned_data.get('section')
        school_class = search_form.cleaned_data.get('school_class')
        subject = search_form.cleaned_data.get('subject')
        
        if search_query:
            books = books.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(subject__icontains=search_query) |
                Q(publisher__icontains=search_query)
            )
        
        if section:
            books = books.filter(section=section)
        
        if school_class:
            books = books.filter(school_class=school_class)
            
        if subject:
            books = books.filter(subject=subject)
    
    # Add offer count to each book
    books = books.annotate(offer_count=Count('offers', filter=Q(offers__is_active=True)))
    
    # Pagination
    paginator = Paginator(books.order_by('school_class', 'subject', 'title'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_books': books.count(),
        'search_query': search_form.cleaned_data.get('search', '') if search_form.is_valid() else '',
    }
    return render(request, 'books/school_book_list.html', context)

def school_book_detail(request, pk):
    """Details eines Schulbuchs mit allen verfügbaren Angeboten"""
    school_book = get_object_or_404(SchoolBook, pk=pk, is_active=True)
    
    # Get all active offers for this book
    offers = StudentOffer.objects.filter(
        school_book=school_book, 
        is_active=True
    ).select_related('seller').order_by('price')
    
    context = {
        'school_book': school_book,
        'offers': offers,
        'user_can_offer': request.user.is_authenticated,
    }
    return render(request, 'books/school_book_detail.html', context)

@login_required
def create_student_offer(request, book_id=None):
    """Neues Angebot für ein Schulbuch erstellen"""
    initial_book = None
    if book_id:
        initial_book = get_object_or_404(SchoolBook, pk=book_id, is_active=True)
    
    if request.method == 'POST':
        form = StudentOfferForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.seller = request.user
            offer.save()
            messages.success(request, f'Your offer for "{offer.school_book.title}" has been created successfully!')
            return redirect('school_book_detail', pk=offer.school_book.pk)
    else:
        form = StudentOfferForm(user=request.user, initial_book=initial_book)
    
    context = {
        'form': form,
        'initial_book': initial_book,
    }
    return render(request, 'books/create_student_offer.html', context)

@login_required
def book_selection(request):
    """Buchauswahl-Seite mit Filtern"""
    books = SchoolBook.objects.filter(is_active=True)
    
    # Filter form
    filter_form = BookSelectionForm(request.GET)
    if filter_form.is_valid():
        section = filter_form.cleaned_data.get('section')
        school_class = filter_form.cleaned_data.get('school_class')
        subject = filter_form.cleaned_data.get('subject')
        
        if section:
            books = books.filter(section=section)
        if school_class:
            books = books.filter(school_class=school_class)
        if subject:
            books = books.filter(subject=subject)
    
    # Add offer count
    books = books.annotate(offer_count=Count('offers', filter=Q(offers__is_active=True)))
    
    # Pagination
    paginator = Paginator(books.order_by('school_class', 'subject', 'title'), 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'total_books': books.count(),
    }
    return render(request, 'books/book_selection.html', context)

@login_required
def my_student_offers(request):
    """Meine Angebote anzeigen"""
    offers = StudentOffer.objects.filter(
        seller=request.user
    ).select_related('school_book').order_by('-created_at')
    
    context = {
        'offers': offers,
    }
    return render(request, 'books/my_student_offers.html', context)

@login_required
def edit_student_offer(request, pk):
    """Angebot bearbeiten"""
    offer = get_object_or_404(StudentOffer, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = StudentOfferForm(request.POST, request.FILES, instance=offer, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your offer has been updated successfully!')
            return redirect('school_book_detail', pk=offer.school_book.pk)
    else:
        form = StudentOfferForm(instance=offer, user=request.user)
    
    context = {
        'form': form,
        'offer': offer,
    }
    return render(request, 'books/edit_student_offer.html', context)

@login_required
def delete_student_offer(request, pk):
    """Angebot löschen"""
    offer = get_object_or_404(StudentOffer, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        school_book = offer.school_book
        offer.delete()
        messages.success(request, 'Your offer has been deleted successfully!')
        return redirect('school_book_detail', pk=school_book.pk)
    
    context = {
        'offer': offer,
    }
    return render(request, 'books/delete_student_offer.html', context)

@login_required
def mark_as_sold(request, pk):
    """Angebot als verkauft markieren"""
    offer = get_object_or_404(StudentOffer, pk=pk, seller=request.user)
    
    offer.is_sold = True
    offer.is_active = False
    offer.save()
    
    messages.success(request, f'"{offer.school_book.title}" has been marked as sold!')
    return redirect('my_student_offers')

# Legacy views für Rückwärtskompatibilität
def offer_list(request):
    """Legacy view - redirect to new school book list"""
    return redirect('school_book_list')

def offer_detail(request, pk):
    """Legacy view - try to find corresponding school book offer"""
    try:
        offer = get_object_or_404(Offer, pk=pk)
        return render(request, 'books/legacy_offer_detail.html', {'offer': offer})
    except:
        return redirect('school_book_list')

@login_required
def create_offer(request):
    """Legacy view - redirect to book selection"""
    return redirect('book_selection')

@login_required
def my_offers(request):
    """Legacy view - redirect to new student offers"""
    return redirect('my_student_offers')

@login_required
def edit_offer(request, pk):
    """Legacy view"""
    try:
        offer = get_object_or_404(Offer, pk=pk, seller=request.user)
        return render(request, 'books/legacy_edit_offer.html', {'offer': offer})
    except:
        return redirect('my_student_offers')

@login_required
def delete_offer(request, pk):
    """Legacy view"""
    try:
        offer = get_object_or_404(Offer, pk=pk, seller=request.user)
        if request.method == 'POST':
            offer.delete()
            messages.success(request, 'Offer deleted successfully!')
            return redirect('my_student_offers')
        return render(request, 'books/legacy_delete_offer.html', {'offer': offer})
    except:
        return redirect('my_student_offers')