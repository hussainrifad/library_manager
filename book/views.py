from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, BookCategory, Review
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from account.models import UserInformation, BorrowItem
from django.urls import reverse_lazy
from decimal import Decimal
from .forms import ReviewForm
# Create your views here.

class BooksView(ListView):
    template_name = 'books.html'
    context_object_name = 'books'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            cate = BookCategory.objects.get(slug=slug)
            return Book.objects.filter(category=cate)
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BookCategory.objects.all()
        return context

class BookDetailsView(DetailView):
    template_name = 'book_details.html'
    model = Book
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.get(pk=self.kwargs.get('pk'))
        try:
            borrowed = BorrowItem.objects.get(book=book)
            context['borrowed'] = True
        except:
            borrowed = None
            context['borrowed'] = False
        return context

    
class CreateReview(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'reviews.html'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get('id')
        context['reviews'] = Review.objects.filter(book_id=book_id)
        return context
    
    def form_valid(self, form):
        print('working')
        Review.objects.create(review=form.cleaned_data.get('review'), reviewer=self.request.user, book_id=self.kwargs.get('id'))
        return redirect('books')
    
    def form_invalid(self, form):
        return super().form_invalid(form=form)



def add_to_list(request, id):
    book = Book.objects.get(id=id)
    user = request.user
    if book.price > user.information.balance:
        return redirect('deposite')

    user.information.balance -= Decimal(book.price)
    user.information.save()
    BorrowItem.objects.create(book=book, borrowed_by=user)
    return redirect('homepage')