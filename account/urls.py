from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterFormView.as_view(), name='register'),
    path('profile/', views.UserUpdateView.as_view(), name='profile'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.userLogOut, name='logout'),
    path('deposite/', views.DepositeView.as_view(), name='deposite'),
    path('borrow_list/', views.BorrowedListView.as_view(), name='borrowlist')
]