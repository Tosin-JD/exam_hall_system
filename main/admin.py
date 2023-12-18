from django.contrib import admin
from .models import Course, Offer, TimeTable, Seat, Hall

# Register your models here.
admin.site.register(Course)
admin.site.register(Offer)
admin.site.register(TimeTable)
admin.site.register(Seat)
admin.site.register(Hall)


