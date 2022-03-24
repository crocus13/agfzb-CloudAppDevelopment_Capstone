from django.contrib import admin
# from .models import related models
from .models import CarModel, CarMake


# Register your models here.
# class CarMakeAdmin(admin.ModelAdmin):
#     fields = ['name', 'description']
#     admin.site.register(CarMake, CarMakeAdmin)
#     admin.site.register(CarModel)


# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# # CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['name', 'year', 'carMake', 'dealerId', 'type']
admin.site.register(CarModel, CarModelAdmin)
    




# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    inlines = [CarModelInline]
admin.site.register(CarMake,CarMakeAdmin)
   

# # Register models here

# admin.site.register(CarMake, CarMakeAdmin)
# admin.site.register(CarModel,CarMakeAdmin)

# admin.site.register(CarMake)
# admin.site.register(CarModel)