from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie
from .forms import MovieForm

# Create your views here.


@login_required
def movies(request):
    """
    Displays a list of all movies.

    This view retrieves all movie objects from the database and renders them
    on the movies list page. Access to this view is restricted to authenticated
    users.

    :param request: The HTTP request object
    :return: An HTTP response object with the list of movies
    """
    movies_list = Movie.objects.all()
    return render(request, 'movies-list.html', {
        'movies': movies_list
    })


@login_required
def movie_detail(request, pk):
    """
    Handles the display of a single movie.

    This view retrieves a movie object using the provided primary key (pk) and
    renders the movie detail page with the movie's data. Access to this view
    is restricted to authenticated users.

    :param request: The HTTP request object
    :param pk: The primary key of the movie to display
    :return: An HTTP response object with the movie details
    """

    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movie-detail.html', {
        'movie': movie
    })


@login_required
def movie_create(request):
    """
    Handles the creation of a new movie.

    If the request method is GET, this view renders the movie create page with
    a blank form. If the request method is POST, this view creates a new movie
    with the given data and redirects to the movies list. Otherwise, this view
    renders the movie create page with an error message.

    :param request: The HTTP request object
    :return: An HTTP response object
    """
    if request.method == 'GET':
        return render(request, 'movie-create.html', {
            'form': MovieForm
        })

    elif request.method == 'POST':
        try:
            form = MovieForm(request.POST, request.FILES)
            form.save()
            return redirect('movies:movies_list')
        except ValueError:
            return render(request, 'movie-create.html', {
                'form': form,
                'error': 'Error creating movie'
            })

    return render(request, 'movie-create.html', {
        'form': MovieForm,
        'error': 'Invalid HTTP method'
    })


@login_required
def movie_update(request, pk):
    """
    Handles the update of a single movie.

    If the request method is GET, this view renders the movie update page
    with the movie's data pre-filled in the form. If the request method is
    POST, this view updates the movie with the given primary key and redirects
    to the movies list. Otherwise, this view renders the movie update page
    with an error message.

    :param request: The HTTP request object
    :param pk: The primary key of the movie to update
    :return: An HTTP response object
    """

    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=pk)
        form = MovieForm(instance=movie)
        return render(request, 'book-create.html', {
            'form': form
        })

    elif request.method == 'POST':
        movie = get_object_or_404(movie, pk=pk)
        try:
            form = MovieForm(request.POST, request.FILES, instance=movie)
            form.save()
            return redirect('movies:movies_list')
        except ValueError:
            return render(request, 'movie-create.html', {
                'form': form,
                'error': 'Error updating movie'
            })


@login_required
def movie_delete(request, pk):
    """
    Handles the deletion of a single movie.

    If the request method is POST, this view deletes the movie with the given
    primary key and redirects to the movies list. Otherwise, this view renders
    the movie delete page with the delete button.

    :param request: The HTTP request object
    :param pk: The primary key of the movie to delete
    :return: An HTTP response object
    """
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movies:movies_list')
