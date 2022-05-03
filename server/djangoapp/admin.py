from django.contrib import admin

from .models import CarMake, CarModel



# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2



# # # CarModelAdmin class
# class CarModelAdmin(admin.ModelAdmin):
#     fields = ['name', 'year', 'carMake', 'dealerId', 'type']
# # admin.site.register(CarModel, CarModelAdmin)
    
class CarModelAdmin(admin.ModelAdmin):

    list_display =  ('name', 'year', 'make', 'type')

    list_filter = ['year']

    search_fields = ['name', 'type']



# CarMakeAdmin class with CarModelInline
# class CarMakeAdmin(admin.ModelAdmin):
#     inlines = [CarModelInline]


class CarMakeAdmin(admin.ModelAdmin):

    inlines = [CarModelInline]

    list_display = ('name', 'description')
 

# Register your models here.
# admin.site.register(CarMake, CarMakeAdmin)
# admin.site.register(CarModel, CarModelAdmin)
# admin.site.register(CarModel)

admin.site.register(CarMake, CarMakeAdmin)

admin.site.register(CarModel, CarModelAdmin)

