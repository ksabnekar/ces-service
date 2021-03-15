from django.db import models
from django.utils import timezone

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    cell_phone = models.CharField(max_length=50)
    start_date = models.DateField(default=timezone.now)
    graduation_date = models.DateField(default=timezone.now)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

class Course(models.Model):
    course_name = models.CharField(max_length=50)
    professor = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    course_type = models.CharField(max_length=30)
    credits = models.IntegerField()

    def created(self):
        self.save()

    def updated(self):
        self.save()


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollment_course')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollment_student')
    semester_name = models.CharField(max_length=30)
    start_date = models.DateField(default=timezone.now, blank=True, null=True)
    end_date = models.DateField(default=timezone.now, blank=True, null=True)
    status = models.CharField(max_length=50)
    grade = models.CharField (max_length=20)

    def created(self):
        self.start_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.student)
