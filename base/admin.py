from django.contrib import admin

# Register your models here.
from .models import Tasks,Location,Category,UserData
admin.site.register(Tasks)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(UserData)