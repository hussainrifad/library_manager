from django.db import models
from django.contrib.auth.models import User
from book.models import Book
from .constants import GENDER
# Create your models here.

class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='information')
    institution = models.CharField(max_length=128, blank=True, null=True)
    group = models.CharField(max_length=32, blank=True, null=True)
    grade = models.IntegerField()
    gender = models.CharField(max_length=16, choices=GENDER)
    country = models.CharField(max_length=128)
    birth_date = models.DateField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)
    balance = models.DecimalField(max_digits=12, default=0, decimal_places=2)

class BorrowItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.name