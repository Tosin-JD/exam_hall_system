# main.models.py
from django.db import models
from accounts.models import Student, Invigilator


def assign_students_to_seats(course_code):
    # Retrieve the course based on the course code
    course = Course.objects.get(code=course_code)

    # Retrieve all the halls that offer the specified course
    halls_with_course = Hall.objects.filter(courses=course)

    # Iterate through each hall and assign students to seats
    for hall in halls_with_course:
        # Get the total capacity of the hall
        hall_capacity = hall.capacity

        # Get the number of students offering the course
        num_students_offering_course = TimeTable.objects.filter(course=course).count()

        # Check if the hall has enough capacity for the students
        if num_students_offering_course <= hall_capacity:
            # Retrieve the seats in the hall
            seats_in_hall = Seat.objects.filter(hall=hall)

            # Check if there are enough seats for the students
            if num_students_offering_course <= seats_in_hall.count():
                # Retrieve the students for the course
                students_for_course = TimeTable.objects.filter(course=course).values_list('student', flat=True)

                # Iterate through the seats and assign students
                for index, seat in enumerate(seats_in_hall):
                    if index < num_students_offering_course:
                        # Assign the student to the seat
                        seat.student = Student.objects.get(pk=students_for_course[index])
                        seat.save()
                        

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=8)

    def __str__(self):
        return self.name

class TimeTable(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_date = models.DateField()
    exam_time = models.TimeField()

    def __str__(self):
        return f"{self.student} - {self.course} - {self.exam_date} {self.exam_time}"

# models.py

class Seat(models.Model):
    hall = models.ForeignKey('Hall', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    position_x = models.IntegerField()
    position_y = models.IntegerField()

    def __str__(self):
        if self.student:
            return f"{self.student} - Hall: {self.hall}, Seat: ({self.position_x}, {self.position_y})"
        else:
            return f"Empty Seat - Hall: {self.hall}, Seat: ({self.position_x}, {self.position_y})"


class Hall(models.Model):
    invigilators = models.ManyToManyField(Invigilator, blank=True)
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    courses = models.ManyToManyField(Course)

    def __str__(self):
        invigilator_names = ', '.join(str(invigilator) for invigilator in self.invigilators.all())
        return f"{self.name} - Invigilators: {invigilator_names}"
