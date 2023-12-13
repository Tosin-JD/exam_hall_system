# main/management/commands/populate_sample_data.py
from django.core.management.base import BaseCommand
from main.models import Course, Hall, Seat, TimeTable
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

        # Create sample students
        student1 = Student.objects.create(username='student1', email='student1@example.com')
        student2 = Student.objects.create(username='student2', email='student2@example.com')
        student3 = Student.objects.create(username='student3', email='student3@example.com')

        # Create sample halls
        hall1 = Hall.objects.create(name='Hall A', capacity=50)
        hall2 = Hall.objects.create(name='Hall B', capacity=30)

        # Assign courses to halls
        hall1.courses.set([course1, course2])
        hall2.courses.set([course2, course3])

        # Create sample invigilators
        invigilator1 = Invigilator.objects.create(username='invigilator1', email='invigilator1@example.com')
        invigilator2 = Invigilator.objects.create(username='invigilator2', email='invigilator2@example.com')

        # Assign invigilators to halls
        hall1.invigilators.set([invigilator1, invigilator2])

        # Create sample seats in Hall A
        for i in range(1, hall1.capacity + 1):
            Seat.objects.create(hall=hall1, position_x=i, position_y=1)

        # Create sample seats in Hall B
        for i in range(1, hall2.capacity + 1):
            Seat.objects.create(hall=hall2, position_x=i, position_y=1)

        # Create sample timetable entries
        for student in [student1, student2, student3]:
            for course in [course1, course2, course3]:
                exam_date = timezone.now().date()
                exam_time = timezone.now().time()
                TimeTable.objects.create(student=student, course=course, exam_date=exam_date, exam_time=exam_time)

        self.stdout.write(self.style.SUCCESS('Sample data populated successfully'))
