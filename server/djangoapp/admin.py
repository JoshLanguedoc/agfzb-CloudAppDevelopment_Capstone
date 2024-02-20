from django.contrib import admin
# from .models import related models
from .models import CarMake
from .models import CarModel

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5


# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['name', 'make', 'trimlevel', 'bodytype', 'year', 'mileage', 'exteriorcolour', 'interiorcolour', 'engine', 'fueltype', 'transmissiontype', 'drivetraintype', 'description']



# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name','country', 'description', 'parentcompany']
    inlines = [CarModelInline]



# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
