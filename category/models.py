from django.db import models

# Create your models here.

class BookCategory(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField()
    