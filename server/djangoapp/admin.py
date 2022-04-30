from django.contrib import admin
from .models import CarModel, CarMake
# from .models import *



# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5




# # # CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['name', 'year', 'carMake', 'dealerId', 'type']
# admin.site.register(CarModel, CarModelAdmin)
    


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

 

# Register your models here.
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
# admin.site.register(CarModel)


