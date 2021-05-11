from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import CustomUser 

class CustomUserAdmin(UserAdmin):
    add_form= UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display=['email', 'username', 'age', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)
