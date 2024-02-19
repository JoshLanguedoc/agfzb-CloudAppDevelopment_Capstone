from django.contrib import admin
# from .models import related models
from .models import CarMake
from .models import CarModel

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
admin.site.register(CarMake)
admin.site.register(CarModel)
