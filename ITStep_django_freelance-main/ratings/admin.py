from django.contrib import admin
from ratings.models import RatingOrder


@admin.register(RatingOrder)
class RatingOrderAdmin(admin.ModelAdmin):
    list_display = ("order", "user", "testimonial") 
    


# Register your models here.
