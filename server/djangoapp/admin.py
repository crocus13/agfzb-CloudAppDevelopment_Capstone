from django.contrib import admin
# from .models import related models
# from .models import CarModel, CarMake
from .models import *



# Register your models here.


# CarModelInline class
# class CarModelInline(admin.StackedInline):
#     model = CarModel
#     extra = 5

# # # CarModelAdmin class
# class CarModelAdmin(admin.ModelAdmin):
#     fields = ['name', 'year', 'carmake', 'dealerid', 'cartype']
# admin.site.register(CarModel, CarModelAdmin)
    




# # CarMakeAdmin class with CarModelInline
# class CarMakeAdmin(admin.ModelAdmin):
#     fields = ['name', 'description']
#     inlines = [CarModelInline]
# admin.site.register(CarMake,CarMakeAdmin)
   

# # Register models here

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

admin.site.register(CarMake, CarMakeAdmin)
# admin.site.register(CarModel)
admin.site.register(CarModel, CarModelAdmin)

