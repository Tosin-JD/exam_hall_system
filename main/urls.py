# main/urls.py

from django.urls import path
from .views import (
    CourseCreateView,
    TimeTableCreateView,
    SeatCreateView,
    HallCreateView,
)

app_name = "main"

urlpatterns = [
    path('add-course/', CourseCreateView.as_view(), name='create_course'),
    path('add-timetable/', TimeTableCreateView.as_view(), name='create_timetable'),
    path('add-seat/', SeatCreateView.as_view(), name='create_seat'),
    path('add-hall/', HallCreateView.as_view(), name='create_hall'),
    # Add URL patterns for listing views or any other views you may have
]
