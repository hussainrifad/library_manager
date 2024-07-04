from .models import Book
from django import forms
from .models import Review


class BookCategoryForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'category', 'image', 'author', 'description']

class ReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'rows':5}))
    class Meta:
        model = Review
        fields = ['review']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : (
                    'appearance-none block my-5 w-full md:w-1/2 bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })