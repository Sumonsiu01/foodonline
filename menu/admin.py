from django.contrib import admin
from .models import Category, FoodItem


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'vendor', 'created_at', 'updated_at')
    search_fields = ('category_name', 'vendor__user__first_name', 'vendor__user__last_name')


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)}
    list_display = ('food_title', 'category', 'vendor', 'price', 'is_available')
    search_fields = ('food_title', 'category__category_name', 'vendor__user__first_name', 'vendor__user__last_name')
    list_filter = ('is_available',)  # ✅ এক আইটেমের টাপলে শেষে কমা (,) দেওয়া বাধ্যতামূলক


admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)