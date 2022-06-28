from django.contrib import admin
from .models import CarModel,CarMake

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarModel,CarModelAdmin)
admin.site.register(CarMake,CarMakeAdmin)