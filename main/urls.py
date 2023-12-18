# main/urls.py

from django.urls import path
from .views import (
    hall_seats_view,
    AllocateSeatsView,
    CourseCreateView,
    TimeTableCreateView,
    SeatCreateView,
    HallCreateView,
    AdminDashboardView,
)

app_name = "main"

urlpatterns = [
    path('allocated-student-seats/', hall_seats_view, name='allocated_seats'),
    path('allocate-seats/', AllocateSeatsView.as_view(), name='allocate'),
    path('courses/', CourseCreateView.as_view(), name='courses'),
    path('add-timetable/', TimeTableCreateView.as_view(), name='create_timetable'),
    path('seats/', SeatCreateView.as_view(), name='seats'),
    path('halls/', HallCreateView.as_view(), name='halls'),
    path('timetables/', TimeTableCreateView.as_view(), name='timetables'),
    path('allotments/', HallCreateView.as_view(), name='allotments'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
]
