# main.models.py
from django.db import models
from accounts.models import Student, Invigilator

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