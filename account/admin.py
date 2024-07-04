from django.contrib import admin
from .models import UserInformation, BorrowItem

# Register your models here.
admin.site.register(UserInformation)
admin.site.register(BorrowItem)