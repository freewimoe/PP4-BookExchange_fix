from django.shortcuts import render

def book_list(request):
    return render(request, 'books/book_list.html')
