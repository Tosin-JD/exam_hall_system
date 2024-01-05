# main/management/commands/populate_sample_data.py
from django.core.management.base import BaseCommand
from main.models import Course, Offer, Hall, Seat, TimeTable
from accounts.models import Student, Invigilator
from django.utils import timezone
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Create sample courses
        course1 = Course.objects.create(name='Mathematics', code='MTH177', department="Mathematics")
        course2 = Course.objects.create(name='Logic', code='MTH141', department="Mathematics")
        course3 = Course.objects.create(name='Statistics', code='MTH201', department="Mathematics")
        course4 = Course.objects.create(name='Probality', code='MTH111', department="Mathematics")
        course5 = Course.objects.create(name='Physics', code='PHYS101', department="Physics")
        course6 = Course.objects.create(name='Computer Science', code='CS101', department="Mathematics")
        course7 = Course.objects.create(name='Biology', code='BIO101', department="Biology")
        course8 = Course.objects.create(name='Chemistry', code='CHM101', department="Chemistry")
        course9 = Course.objects.create(name='Food Technology', code='FTH101', department="Food Technology")
        course10 = Course.objects.create(name='Electrical Engineering', code='EEG101', department="Electrical Engineering")
        course11 = Course.objects.create(name='Science Lab Tech', code='SLT101', department="Science Lab Tech")
        course12 = Course.objects.create(name='Mechanical Engineering', code='MEG101', department="Mechanical Engineering")
        course13 = Course.objects.create(name='Agricultural Science', code='AGS101', department="Agriculture")
        course14 = Course.objects.create(name='Medicine', code='MMD101', department="Medicine")
        course15 = Course.objects.create(name='Office Technology', code='OTM101', department="Office Technology")
        course16 = Course.objects.create(name='Banking and Finance', code='BFN101', department="Banking")
        course17 = Course.objects.create(name='Accounting', code='ACC101', department="Account")
        course18 = Course.objects.create(name='History', code='HST101', department="Art")
        course19 = Course.objects.create(name='Government', code='GST201', department="Art")
        course20 = Course.objects.create(name='Entrepreneurship', code='EED232', department="General Studies")

        student_list = []
        for i in range(1, 101):
            username = f'student{i}'
            email = f'student{i}@example.com'
            student = Student.objects.create(username=username, email=email)
            student_list.append(student)

        # Create sample halls
        hall1 = Hall.objects.create(name='Hall A', capacity=50, description="New Building", num_columns=5, num_rows=10)
        hall2 = Hall.objects.create(name='Hall B', capacity=42, description="Old Building", num_columns=7, num_rows=6)
        hall3 = Hall.objects.create(name='Hall C', capacity=40, description="New Building", num_columns=4, num_rows=10)
        hall4 = Hall.objects.create(name='Hall D', capacity=36, description="Old Building", num_columns=6, num_rows=6)
        hall5 = Hall.objects.create(name='Hall E', capacity=50, description="New Building", num_columns=5, num_rows=10)
        hall6 = Hall.objects.create(name='Hall F', capacity=72, description="Old Building", num_columns=6, num_rows=12)
        
        # Create sample invigilators
        invigilator1 = Invigilator.objects.create(username='invigilator1', email='invigilator1@example.com')
        invigilator2 = Invigilator.objects.create(username='invigilator2', email='invigilator2@example.com')

        # Assign invigilators to halls
        # hall1.invigilators.set([invigilator1, invigilator2])
        halls = [hall1, hall2, hall3, hall4, hall5, hall6]
        
        for hall in halls:
            for i in range(1, hall.num_columns + 1):
                for j in range(1, hall.num_rows + 1):
                    Seat.objects.create(hall=hall, position_x=i, position_y=j)
                    
        courses = [course1, course2, course3, course4, course5, 
                   course6, course7, course8, course9, course10,
                   course11, course12, course13, course14, course15,
                   course16, course17, course18, course19, course20,]

        # Create sample student offer
        for student in student_list:
            # Decide the number of courses for the student
            num_courses = random.choice([3, 3, 3])  # 0.3 chance of 2, 0.3 chance of 2, and 0.4 chance of 3
            
            # Shuffle the courses list and take the first 'num_courses'
            selected_courses = random.sample(courses, num_courses)
            
            for course in selected_courses:
                
                Offer.objects.create(course=course, student=student)
                
                
        # Create sample timetable entries
        courses = Course.objects.all()
        exam_date = "2023-12-21"
        exam_time = ["08:00:00", "11:00:00", "14:00:00"]
        count = 0
        for course in courses:
            randomly_selected_time = random.choice(exam_time)
            TimeTable.objects.create(course=course, exam_date=exam_date, exam_time=randomly_selected_time)
            if (count % 3 == 0):
                exam_date = datetime.strptime(exam_date, "%Y-%m-%d").date()
                exam_date = str(exam_date + timedelta(days=1))
            count += 1

        self.stdout.write(self.style.SUCCESS('Sample data populated successfully'))
