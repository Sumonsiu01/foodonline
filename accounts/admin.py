from django.contrib import admin

from .models import User,UserProfile

from django.contrib.auth.admin import UserAdmin



# Register your models here.

class CustomUserAdmin(UserAdmin):
  list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
  ordering = ('-date_joined',)
  filter_horizontal = ()
  list_filter = ()
  fieldsets = ()

## codegula chatgpt re dile kuntar mane ki bole dibe.But apatoto ei code er karone admin panel a keu password update korte parbe na. karon admin.py file a CustomUserAdmin class er moddhe fieldsets, list_filter, filter_horizontal empty rakha hoyeche. jodi apni chaen je admin panel theke user password update korte parbe tahole ei class er moddhe fieldsets, list_filter, filter_horizontal properly set korte hobe.   

admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile)