# main.views.py

from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView


from django.urls import reverse_lazy
from .models import Course, TimeTable, Seat, Hall
from .forms import CourseForm, TimeTableForm, SeatForm, HallForm
from accounts.models import CustomUser
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.




from django.http import HttpResponse
from .models import assign_students_to_seats


class IndexView(TemplateView):
    template_name = 'index.html'
    
    
class AboutView(TemplateView):
    template_name = 'about.html'
    
    
class ContactView(TemplateView):
    template_name = 'contact.html'
    
    
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser  # Only allow superusers (admin)

class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'create_course.html'
    success_url = reverse_lazy('course_list')  # Add a URL pattern for listing courses

class TimeTableCreateView(CreateView):
    model = TimeTable
    form_class = TimeTableForm
    template_name = 'create_timetable.html'
    success_url = reverse_lazy('timetable_list')  # Add a URL pattern for listing timetables

class SeatCreateView(CreateView):
    model = Seat
    form_class = SeatForm
    template_name = 'create_seat.html'
    success_url = reverse_lazy('seat_list')  # Add a URL pattern for listing seats

class HallCreateView(CreateView):
    model = Hall
    form_class = HallForm
    template_name = 'create_hall.html'
    success_url = reverse_lazy('hall_list')
    

def assign_students_to_seats_view(request, course_code):
    assign_students_to_seats(course_code)
    return HttpResponse(f"Students assigned to seats for course with code: {course_code}")
