from django.shortcuts import render
from .models import Book, BookInstance, Author
from django.views import generic

def index(request):
    #list_books = Book.objects.all()
    #context = {'all_books': list_books}
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context, content_type="text/html", status=200)

class BookListView(generic.ListView):
    model = Book

    context_object_name = 'book_list'   # your own name for the list as a template

    queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing

    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own

    def get_queryset(self):
        return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

def book_detail(request, id):
    book = Book.objects.get(id__exact=id)
    context = {'book': book}

    return render(request, 'book_detail.html', context=context, content_type="text/html", status=200)