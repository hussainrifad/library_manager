from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth import logout

# Create your views here.

class HomeTemplateView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['message'] = 'This is home page'
        return context