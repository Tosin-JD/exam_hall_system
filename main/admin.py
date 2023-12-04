from django.contrib import admin
from .models import Course, TimeTable, Seat, Hall

# Register your models here.
admin.site.register(Course)
admin.site.register(TimeTable)
admin.site.register(Seat)
admin.site.register(Hall)


