from django.contrib import admin
# from .models import related models
from .models import CarModel, CarMake


# Register your models here.
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    admin.site.register(CarMake, CarMakeAdmin)
    admin.site.register(CarModel)


# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# # CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['name', 'year', 'carmake', 'dealerId', 'type']
    admin.site.register(CarModel, CarModelAdmin)




# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    admin.site.register(CarMake, CarMakeAdmin)
    inlines = [CarModelInline]

# Register models here

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)