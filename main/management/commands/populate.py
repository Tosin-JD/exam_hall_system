# main/management/commands/populate_sample_data.py
from django.core.management.base import BaseCommand
from main.models import Faculty, Department, Course, Offer, Hall, Seat, TimeTable
from accounts.models import Student, Invigilator
from django.utils import timezone
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Create sample faculties
        faculty1 = Faculty.objects.create(name='Arts and Humanities')
        faculty2 = Faculty.objects.create(name='Science')
        faculty3 = Faculty.objects.create(name='Social Sciences')
        
        department1 = Department.objects.create(name='Literature', faculty=faculty1)
        department2 = Department.objects.create(name='Physics', faculty=faculty2)
        department3 = Department.objects.create(name='Sociology', faculty=faculty3)
        department4 = Department.objects.create(name='Chemistry', faculty=faculty2)
        department5 = Department.objects.create(name='Mathematics', faculty=faculty2)
        
        # Create sample courses
        course1 = Course.objects.create(name='Introduction to Literary Analysis', code='LIT101', department= department1)
        course2 = Course.objects.create(name='American Literature Survey', code='LIT201', department= department1)
        course3 = Course.objects.create(name='British Romantic Poetry', code='LIT301', department= department1)
        course4 = Course.objects.create(name='Contemporary World Fiction', code='LIT401', department= department1)
        course5 = Course.objects.create(name='Shakespearean Tragedies', code='LIT501', department= department1)
        
        course6 = Course.objects.create(name='Classical Mechanics', code='PHY101', department=department2)
        course7 = Course.objects.create(name='Quantum Mechanics', code='PHY201', department=department2)
        course8 = Course.objects.create(name='Electromagnetism', code='PHY301', department=department2)
        course9 = Course.objects.create(name='Thermodynamics and Statistical Mechanics', code='PHY401', department=department2)
        course10 = Course.objects.create(name='Astrophysics', code='PHY501', department=department2)
        
        course11 = Course.objects.create(name='General Chemistry', code='CHEM101', department=department4)
        course12 = Course.objects.create(name='Organic Chemistry', code='CHEM201', department=department4)
        course13 = Course.objects.create(name='Inorganic Chemistry', code='CHEM301', department=department4)
        course14 = Course.objects.create(name='Physical Chemistry', code='CHEM401', department=department4)
        course15 = Course.objects.create(name='Analytical Chemistry', code='CHEM501', department=department4)
        
        course16 = Course.objects.create(name='Calculus I', code='MATH101', department=department5)
        course17 = Course.objects.create(name='Linear Algebra', code='MATH201', department=department5)
        course18 = Course.objects.create(name='Differential Equations', code='MATH301', department=department5)
        course19 = Course.objects.create(name='Abstract Algebra', code='MATH401', department=department5)
        course20 = Course.objects.create(name='Real Analysis', code='MATH501', department=department5)
        
        course21 = Course.objects.create(name='Introduction to Sociology', code='SOC101', department=department_of_sociology)
        course22 = Course.objects.create(name='Social Research Methods', code='SOC201', department=department_of_sociology)
        course23 = Course.objects.create(name='Gender and Society', code='SOC301', department=department_of_sociology)
        course24 = Course.objects.create(name='Sociology of Deviance', code='SOC401', department=department_of_sociology)
        course25 = Course.objects.create(name='Contemporary Social Issues', code='SOC501', department=department_of_sociology)

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
                   course16, course17, course18, course19, course20,
                   course21, course22, course23, course24, course25, ]

        # Create sample student offer
        # for student in student_list:
        #     # Decide the number of courses for the student
        #     num_courses = random.choice([5, 5, 3])  # 0.3 chance of 2, 0.3 chance of 2, and 0.4 chance of 3
            
        #     # Shuffle the courses list and take the first 'num_courses'
        #     selected_courses = random.sample(courses, num_courses)
            
        #     for course in selected_courses:
        #         Offer.objects.create(course=course, student=student)
                
        # Create sample student offer
        for student in student_list:
            for course in courses:
                Offer.objects.create(course=course, student=student)
                
                
        # Create sample timetable entries
        courses = Course.objects.all()
        exam_date = "2024-01-17"
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
