from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import BookForm

# Create your views here.


@login_required
def books(request):
    """
    Displays a list of all books.

    This view retrieves all book objects from the database and renders them
    on the books list page. Access to this view is restricted to authenticated
    users.

    :param request: The HTTP request object
    :return: An HTTP response object with the list of books
    """

    books_list = Book.objects.all()
    return render(request, 'books-list.html', {
        'books': books_list
    })


@login_required
def book_detail(request, pk):
    """
    Handles the display of a single book.

    If the request method is GET, this view renders the book detail page with
    the book's data pre-filled in the form. If the request method is not GET, this
    view renders the book detail page with an error message.

    :param request: The HTTP request object
    :param pk: The primary key of the book to display
    :return: An HTTP response object
    """
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book-detail.html', {
        'book': book
    })


@login_required
def book_create(request):
    """
    Handles the creation of a new book.

    If the request method is GET, this view renders the book create page with
    a blank form. If the request method is POST, this view creates a new book
    with the given data and redirects to the books list. Otherwise, this view
    renders the book create page with an error message.

    :param request: The HTTP request object
    :return: An HTTP response object
    """
    if request.method == 'GET':
        return render(request, 'book-create.html', {
            'form': BookForm
        })

    elif request.method == 'POST':
        try:
            form = BookForm(request.POST, request.FILES)
            print(request.FILES)
            form.save()
            return redirect('books:books_list')
        except ValueError:
            return render(request, 'book-create.html', {
                'form': form,
                'error': 'Error creating book'
            })

    return render(request, 'book-create.html', {
        'form': BookForm,
        'error': 'Invalid HTTP method'
    })


@login_required
def book_update(request, pk):
    """
    Handles the update of a single book.

    If the request method is GET, this view renders the book update page with
    the book's data pre-filled in the form. If the request method is POST, this
    view updates the book with the given primary key and redirects to the books
    list. Otherwise, this view renders the book update page with the error
    message.

    :param request: The HTTP request object
    :param pk: The primary key of the book to update
    :return: An HTTP response object
    """
    if request.method == 'GET':
        book = get_object_or_404(Book, pk=pk)
        form = BookForm(instance=book)
        return render(request, 'book-create.html', {
            'form': form
        })

    elif request.method == 'POST':
        book = get_object_or_404(Book, pk=pk)
        try:
            form = BookForm(request.POST, request.FILES, instance=book)
            form.save()
            return redirect('books:books_list')
        except ValueError:
            return render(request, 'book-create.html', {
                'form': form,
                'error': 'Error updating book'
            })


@login_required
def book_delete(request, pk):
    """
    Handles the deletion of a single book.

    If the request method is POST, this view deletes the book with the given
    primary key and redirects to the books list. Otherwise, this view renders
    the book detail page with the delete button.

    :param request: The HTTP request object
    :param pk: The primary key of the book to delete
    :return: An HTTP response object
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('books:books_list')
