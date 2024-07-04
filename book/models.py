from django.db import models
from category.models import BookCategory
from django.contrib.auth.models import User
# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE, related_name='book')
    image = models.ImageField(upload_to='book/media/image', blank=True, null=True)
    author = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.IntegerField()
    review = models.TextField(max_length=512)
    creation = models.DateField(auto_now_add=True)
