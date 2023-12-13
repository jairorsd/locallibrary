from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, BookInstance, Author
from django.views import View, generic

class MinhaViewProtegida(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

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

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context, content_type="text/html", status=200)

class BookListView(generic.ListView):
    model = Book

    context_object_name = 'book_list'   # your own name for the list as a template

    template_name = 'catalog/book_list.html'

    paginate_by = 2

    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5] # Get 5 books containing
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(generic.DetailView):
    model = Book
    
    template_name = 'catalog/book_detail.html'

class AuthorListView(generic.ListView):
    model = Author 

    context_object_name = 'author_list'

    template_name = 'catalog/author_list.html'

    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author

    template_name = 'catalog/author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )

from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksByUserWithPermissionListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user_can_mark_returned.html'
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return (
            BookInstance.objects.all()
            .filter(status__exact='o')
            .order_by('due_back')
        )


# class MyView(PermissionRequiredMixin, View):
#     permission_required = 'catalog.can_mark_returned'
#     # Or multiple permissions
#     permission_required = ('catalog.can_mark_returned', 'catalog.change_book')
#     # Note that 'catalog.change_book' is permission
#     # Is created automatically for the book model, along with add_book, and delete_book

# Function views

# from django.contrib.auth.decorators import permission_required

# @login_required
# @permission_required('catalog.can_mark_returned')
# @permission_required('catalog.can_edit', raise_exception=True)
# def my_view(request):
#     # …

# from django.http import Http404

# def book_detail_view(request, primary_key):
#     try:
#         book = Book.objects.get(pk=primary_key)
#     except Book.DoesNotExist:
#         raise Http404('Book does not exist')

#     return render(request, 'catalog/book_detail.html', context={'book': book})


# from django.shortcuts import get_object_or_404

# def book_detail_view(request, primary_key):
#     book = get_object_or_404(Book, pk=primary_key)
#     return render(request, 'catalog/book_detail.html', context={'book': book})