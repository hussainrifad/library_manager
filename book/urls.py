from django.urls import path
from . import views

urlpatterns = [
    path('', views.BooksView.as_view(), name='books'),
    path('<slug:slug>/', views.BooksView.as_view(), name='books_by_cate'),
    path('book/<int:pk>/', views.BookDetailsView.as_view(), name='bookdetails'),
    path('borrow/<int:id>/', views.add_to_list, name='borrowbook'),
    path('review/<int:id>', views.CreateReview.as_view(), name='review')
]