from datetime import date

from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('catalog')


def books_view(request):
    books = Book.objects.all()
    template = 'books/books_list.html'
    context = {'books': books}
    # for book in books:
    #     print(book.pub_date)
    return render(request, template, context)


def books_pages(request, pub_date):
    content = {}
    books = sorted(Book.objects.all(), key=lambda book: book.pub_date)
    for book in books:
        if str(book.pub_date) not in content.keys():
            content[str(book.pub_date)] = [book]
        else:
            content[str(book.pub_date)].append(book)
    paginator = Paginator(list(content.values()), 1)
    dates = list(content.keys())
    page_number = dates.index(pub_date) + 1
    page = paginator.get_page(page_number)
    prev_date_num = page_number-1
    if prev_date_num > 0:
        prev_date = dates[prev_date_num-1]
    else:
        prev_date = None
    next_date_num = page_number+1
    if next_date_num <= paginator.num_pages:
        next_date = dates[next_date_num-1]
    else:
        next_date = None
    template = 'books/books_date.html'
    context = {
        'pub_date': pub_date,
        'prev_date': prev_date,
        'prev_date_num': prev_date_num,
        'next_date': next_date,
        'next_date_num': next_date_num,
        'page': page,
    }
    return render(request, template, context)
