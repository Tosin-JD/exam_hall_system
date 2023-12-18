# main/management/commands/populate_sample_data.py
from django.core.management.base import BaseCommand
from main.models import Course, Offer, Hall, Seat, TimeTable
from accounts.models import Student, Invigilator
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Create sample courses
        course1 = Course.objects.create(name='Mathematics', code='MATH101')
        course2 = Course.objects.create(name='Physics', code='PHYS101')
        course3 = Course.objects.create(name='Computer Science', code='CS101')
        course4 = Course.objects.create(name='Biology', code='CS101')
        course5 = Course.objects.create(name='Food Technology', code='FTH101')
        course6 = Course.objects.create(name='Electrical Engineering', code='EEG101')
        course7 = Course.objects.create(name='Science Lab Tech', code='SLT101')

        student_list = []
        for i in range(1, 501):
            username = f'student{i}'
            email = f'student{i}@example.com'
            student = Student.objects.create(username=username, email=email)
            student_list.append(student)

        # Create sample halls
        hall1 = Hall.objects.create(name='Hall A', capacity=50, description="New Building", num_columns=5, num_rows=10)
        hall2 = Hall.objects.create(name='Hall B', capacity=30, description="Old Building", num_columns=5, num_rows=6)
        hall3 = Hall.objects.create(name='Hall C', capacity=50, description="New Building", num_columns=5, num_rows=10)
        hall4 = Hall.objects.create(name='Hall D', capacity=30, description="Old Building", num_columns=5, num_rows=6)
        hall5 = Hall.objects.create(name='Hall E', capacity=50, description="New Building", num_columns=5, num_rows=10)
        hall6 = Hall.objects.create(name='Hall F', capacity=60, description="Old Building", num_columns=6, num_rows=10)
        
        # Create sample invigilators
        invigilator1 = Invigilator.objects.create(username='invigilator1', email='invigilator1@example.com')
        invigilator2 = Invigilator.objects.create(username='invigilator2', email='invigilator2@example.com')

        # Assign invigilators to halls
        # hall1.invigilators.set([invigilator1, invigilator2])
        halls = [hall1, hall2, hall3, hall4, hall5, hall6]
        
        for hall in halls:
            for i in range(1, hall.num_columns + 1):
                for j in range(1, hall.num_columns + 1):
                    Seat.objects.create(hall=hall, position_x=i, position_y=j)
                    
        courses = [course1, course2, course3, course4, course5, course6, course7]

        # Create sample timetable entries
        for student in student_list:
            for course in courses:
                exam_date = timezone.now().date()
                exam_time = timezone.now().time()
                Offer.objects.create(course=course, student=student)
                TimeTable.objects.create(course=course, exam_date=exam_date, exam_time=exam_time)

        self.stdout.write(self.style.SUCCESS('Sample data populated successfully'))
