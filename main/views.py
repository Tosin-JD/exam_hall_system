# main.views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic import ListView 



from django.urls import reverse_lazy

from .models import Course, Offer, TimeTable, Seat, Hall
from .forms import CourseForm, TimeTableForm, SeatForm, HallForm
from accounts.models import CustomUser, Student
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
import csv
from django.views import View

from django.db.models import Count
import random
from .utils import get_today_courses, list_to_dict

from datetime import datetime, timedelta
from datetime import timedelta
from itertools import combinations, zip_longest
from .models import Course, Offer, TimeTable

from more_itertools import interleave_evenly, zip_equal

from itertools import groupby
from operator import itemgetter
# main/views.py
from django.shortcuts import render
from django.views import View
from .models import Seat, Course, Offer, Hall
import random

from django.views import View
from django.shortcuts import render
from more_itertools import interleave_evenly, chunked
from random import randrange

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve TimeTable data and pass it to the template
        context['timetable_data'] = TimeTable.objects.all()
        return context
    
    
class AboutView(TemplateView):
    template_name = 'about.html'
    
    
class ContactView(TemplateView):
    template_name = 'contact.html'
    
    
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def hall_seats_view(request):
    all_halls = Hall.objects.all()

    hall_seat_data = {}

    for hall in all_halls:
        seats_in_hall = Seat.objects.filter(hall=hall)
        hall_seat_data[hall] = seats_in_hall

    context = {'hall_seat_data': hall_seat_data}
    return render(request, 'main/hall_seats.html', context)


# class AllocateSeatsView(View):
#     template_name = 'main/allocations.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         # Seat.objects.all().update(student=None)
#         all_halls = Hall.objects.all()
#         all_courses = Course.objects.all()
        
#         students_by_course = {}
#         for course in all_courses:
#             students_in_course = Student.objects.filter(offer__course=course)
#             students_by_course[course.name] = list(students_in_course)
        
#         hall_seat_data = {}
        
#         for hall in all_halls:
#             seats_in_hall = Seat.objects.filter(hall=hall)
#             hall_seat_data[hall] = seats_in_hall
        
#         for hall, seats_queryset in hall_seat_data.items():
#             course, students = next(iter(students_by_course.items()), (None, []))
            
#             for seat, student in zip(seats_queryset, students):
#                 seat.student = student
            
#             remaining_seats = seats_queryset[len(students):]
#             for seat in remaining_seats:
#                 seat.student = None 
#             students = students[len(seats_queryset):]
#             students_by_course[course] = students
#         context = {'hall_seat_data': hall_seat_data}
#         return render(request, 'main/hall_seats.html', context)
    
    
class AllocateSeatsView(View):
    template_name = 'main/allocations.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Seat.objects.all().update(student=None)
        
        all_halls = Hall.objects.all()
        all_courses = Course.objects.all()
        
        courses_today = get_today_courses()
        
        students_by_course = {}
        stud_by_co = []
        for course in courses_today:
            students_in_course = Student.objects.filter(offer__course=course)
            students_by_course[course.name] = list(students_in_course)
            stud_by_co.append(tuple(students_in_course))
            
        if not stud_by_co:
            context = {'message': "There are no exams sheduled for today"}
            return render(request, self.template_name, context)
            
        # shuffled_students = list(interleave_evenly(stud_by_co))
        
        hall_seat_data = {}
        
        for hall in all_halls:
            seats_in_hall = Seat.objects.filter(hall=hall)
            hall_seat_data[hall] = seats_in_hall
            
        for hall, seats_queryset in hall_seat_data.items():
            students = next(iter(stud_by_co))
            
            for seat, student in zip(seats_queryset, students):
                # seat.student = None
                seat.student = student
                # seat.save()
            
            remaining_seats = seats_queryset[len(students):]
            for seat in remaining_seats:
                seat.student = None 
            students = students[len(seats_queryset):]
            
            stud_by_co = []
            stud_by_co.append(students)
            # shuffled_students_dict[num] = students
            
        # for hall, seats_queryset in hall_seat_data.items():
        #     course, students = next(iter(students_by_course.items()), (None, []))
        #     print(students)
            
        #     for seat, student in zip(seats_queryset, students):
        #         seat.student = student
                # seat.save()
            
            # remaining_seats = seats_queryset[len(students):]
            # for seat in remaining_seats:
            #     seat.student = None 
            # students = students[len(seats_queryset):]
            # students_by_course[course] = students
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
    

class GenerateTimeTableView(View):
    template_name = 'main/timetables.html'
    
    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        timetable = TimeTable.objects.all()
        form = CourseForm()
        return render(request, self.template_name, {'courses': courses, 'timetable':timetable, 'form': form})

    def post(self, request, *args, **kwargs):
        form = TimeTableForm(request.POST)
        courses = Course.objects.all()
        offers = Offer.objects.select_related('course__department').all()
        
        grouped_courses = Course.objects.values('department').annotate(course_count=Count('id'))

        courses = Course.objects.all().order_by('department')
        
        # courses = Course.objects.all().order_by('department__name', 'name')

        # # Assuming you have the models and queryset as defined in the previous answer

        # # Group courses by department
        # grouped_courses = {}
        # for department, department_courses in groupby(courses, key=lambda x: x.department):
        #     grouped_courses[department] = list(department_courses)
    
        course_list = Course.objects.values_list(
                        'department', flat=True
                    ).distinct()
        
        group_by_department = {}
        group_list = []
        for value in course_list:
            group_by_department[value] = Course.objects.filter(department=value)
            group_list.append(Course.objects.filter(department=value))
    
        exam_date = request.POST.get('exam_date')
        
        exam_time = ["08:00:00", "11:00:00", "14:00:00"]
        count = 0
        TimeTable.objects.all().delete()
        for department in zip_longest(*group_by_department.values()):
            for course in department:
                if datetime.strptime(exam_date, "%Y-%m-%d").date().weekday() < 6:
                    randomly_selected_time = random.choice(exam_time)
                    if course is None:
                        continue
                    TimeTable.objects.create(course=course, exam_date=exam_date, exam_time=randomly_selected_time)
                if (count % 3 == 0):
                    exam_date = datetime.strptime(exam_date, "%Y-%m-%d").date()
                    exam_date = str(exam_date + timedelta(days=1))
                count += 1            
        timetable = TimeTable.objects.all()
        context = {'timetable': timetable, 'form':form}
        return render(request, self.template_name, context)

    

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
        timetable = TimeTable.objects.all()
        form = TimeTableForm()
        return render(request, self.template_name, {'timetable': timetable, 'form': form})

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


class StudentSeatView(LoginRequiredMixin, TemplateView):
    template_name = 'main/student_seat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        student = None
        student_courses = None
        assigned_seat = None

        # if self.request.user.is_authenticated and isinstance(self.request.user, Student):
        if self.request.user.is_authenticated and self.request.user.user_type == "Student":
            student = get_object_or_404(Student, id=self.request.user.id)
            student_courses = student.get_courses()
            student_today_courses = student.get_today_courses()
            assigned_seat = Seat.objects.filter(student=student).first()
        context['student'] = student
        context['student_courses'] = student_courses
        context['student_today_courses'] = student_today_courses
        context['assigned_seat'] = assigned_seat

        return context