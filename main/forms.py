# forms.py

from django import forms
from .models import Course, TimeTable, Seat, Hall
from accounts.models import CustomUser

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']

class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['student', 'course', 'exam_date', 'exam_time']

class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ['hall', 'student', 'position_x', 'position_y']

class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ['name', 'invigilators', 'capacity', 'courses']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'user_type']
