from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserInformationForm, UserInformationUpdateForm, DepositeForm
from .models import UserInformation, BorrowItem
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views.generic import View, CreateView, ListView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from decimal import Decimal
from django.contrib import messages


# Create your views here.

class RegisterFormView(CreateView):
    template_name = 'register.html'
    form_class = UserInformationForm
    success_url = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('profile')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        return super().form_valid(form) # form_valid function call hobe jodi sob thik thake
    
    def form_invalid(self, form):
        return super().form_invalid(form=form)

class UserUpdateView(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserInformationUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserInformationUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})

class UserLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        return redirect('profile')
    
    def get_success_url(self):
        return reverse_lazy('homepage')
    
def userLogOut(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('homepage')

class DepositeView(LoginRequiredMixin, View):
    template_name = 'deposite.html'
    success_url = reverse_lazy('books')
    
    def get(self, request):
        form = DepositeForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = DepositeForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            user_info = UserInformation.objects.get(user=request.user)
            user_info.balance += Decimal(amount)
            user_info.save()
            return redirect('books')
        return render(request, self.template_name, {'form': form})
    
class BorrowedListView(LoginRequiredMixin, ListView):
    model = BorrowItem
    template_name = 'borrowed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_id = self.kwargs.get('id')
        user = User.objects.get(id=object_id)
        context['borrowedItem'] = BorrowItem.objects.filter(borrowed_by=user)
        return context
