# main.views.py

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic import ListView 


from django.urls import reverse_lazy
from .models import Course, Offer, TimeTable, Seat, Hall
from .forms import CourseForm, TimeTableForm, SeatForm, HallForm
from accounts.models import CustomUser, Student
from django.contrib.auth.mixins import UserPassesTestMixin
import csv
from django.views import View

import random

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'
    
    
class AboutView(TemplateView):
    template_name = 'about.html'
    
    
class ContactView(TemplateView):
    template_name = 'contact.html'
    
    
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


# main/views.py
from django.shortcuts import render
from django.views import View
from .models import Seat, Course, Offer, Hall
import random


def hall_seats_view(request):
    all_halls = Hall.objects.all()

    hall_seat_data = {}

    for hall in all_halls:
        seats_in_hall = Seat.objects.filter(hall=hall)
        hall_seat_data[hall] = seats_in_hall

    context = {'hall_seat_data': hall_seat_data}
    return render(request, 'main/hall_seats.html', context)


class AllocateSeatsView(View):
    template_name = 'main/allocations.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Seat.objects.all().update(student=None)
        all_halls = Hall.objects.all()
        all_courses = Course.objects.all()
        
        students_by_course = {}
        for course in all_courses:
            students_in_course = Student.objects.filter(offer__course=course)
            students_by_course[course.name] = list(students_in_course)

        hall_seat_data = {}

        for hall in all_halls:
            seats_in_hall = Seat.objects.filter(hall=hall)
            hall_seat_data[hall] = seats_in_hall
        print(hall_seat_data)
        for hall, seats_queryset in hall_seat_data.items():
            for seat in seats_queryset:
                for course, students in students_by_course.items():
                    for student in students:
                        seat.student = student
                        seat.save()
        context = {'hall_seat_data': hall_seat_data}
        return render(request, 'main/hall_seats.html', context)
    
    
class AdminDashboardView(FormView):
    template_name = 'main/admin_dashboard.html'
    form_class = CourseForm 
    success_url = '/admin/dashboard/'
    def get_form(self, form_class=None):
        form_type = self.request.GET.get('form_type', 'course')
        if form_type == 'course':
            self.form_class = CourseForm
        elif form_type == 'timetable':
            self.form_class = TimeTableForm
        elif form_type == 'seat':
            self.form_class = SeatForm
        elif form_type == 'hall':
            self.form_class = HallForm
        return super().get_form(form_class)

    def form_valid(self, form):
        form.save()
        # Additional logic if needed
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = self.request.GET.get('form_type', 'course')
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
    

class CourseCreateView(View):
    template_name = 'main/courses.html'

    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        form = CourseForm()
        return render(request, self.template_name, {'courses': courses, 'form': form})

    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:courses')

        return render(request, self.template_name, {'form': form})

    def csv_upload(self, csv_file):
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            Course.objects.create(name=row['name'])

    def post(self, request, *args, **kwargs):
        form = CourseForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('main:courses')

        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            self.csv_upload(csv_file)
            return redirect('main:courses')

        return render(request, self.template_name, {'form': form})
    
    

class SeatCreateView(View):
    template_name = 'main/seats.html'

    def get(self, request, *args, **kwargs):
        seats = Seat.objects.all()
        form = SeatForm()
        return render(request, self.template_name, {'seats': seats, 'form': form})

    def post(self, request, *args, **kwargs):
        form = SeatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:seats')

        return render(request, self.template_name, {'form': form})

    def csv_upload(self, csv_file):
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            Seat.objects.create(
                hall=row['hall'],
                student=row['student'],
                position_x=row['position_x'],
                position_y=row['position_y']
            )

    def post(self, request, *args, **kwargs):
        form = SeatForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('main:seats')

        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            self.csv_upload(csv_file)
            return redirect('main:seats')

        return render(request, self.template_name, {'form': form})


class HallCreateView(View):
    template_name = 'main/halls.html'

    def get(self, request, *args, **kwargs):
        halls = Hall.objects.all()
        form = HallForm()
        return render(request, self.template_name, {'halls': halls, 'form': form})

    def post(self, request, *args, **kwargs):
        form = HallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:halls')

        return render(request, self.template_name, {'form': form})

    def csv_upload(self, csv_file):
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            hall = Hall.objects.create(
                name=row['name'],
                capacity=row['capacity'],
                description=row['description'],
                num_columns=row['num_columns'],
                num_rows=row['num_rows']
            )
            # Add courses and invigilators if needed
            # Example: hall.courses.add(course1, course2)
            # Example: hall.invigilators.add(invigilator1, invigilator2)

    def post(self, request, *args, **kwargs):
        form = HallForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('main:halls')

        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            self.csv_upload(csv_file)
            return redirect('main:halls')

        return render(request, self.template_name, {'form': form})
    

class TimeTableCreateView(View):
    template_name = 'main/timetables.html'

    def get(self, request, *args, **kwargs):
        timetable_entries = TimeTable.objects.all()
        form = TimeTableForm()
        return render(request, self.template_name, {'timetable_entries': timetable_entries, 'form': form})

    def post(self, request, *args, **kwargs):
        form = TimeTableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:timetables')

        return render(request, self.template_name, {'form': form})

    def csv_upload(self, csv_file):
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            TimeTable.objects.create(
                course=row['course'],
                exam_date=row['exam_date'],
                exam_time=row['exam_time']
            )

    def post(self, request, *args, **kwargs):
        form = TimeTableForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('main:timetables')

        if 'csv_file' in request.FILES:
            csv_file = request.FILES['csv_file']
            self.csv_upload(csv_file)
            return redirect('main:timetables')

        return render(request, self.template_name, {'form': form})
