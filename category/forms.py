from .models import BookCategory
from django import forms


class BookCategoryForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    
    class Meta:
        model = BookCategory
        fields = ['title']