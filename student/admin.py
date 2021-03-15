from django.contrib import admin
from .models import Student, Course, Enrollment


class StudentList(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'cell_phone', 'start_date', 'graduation_date')
    list_filter = ('name', 'email', 'cell_phone', 'start_date', 'graduation_date')
    search_fields = ('name', 'email')
    ordering = ['name']

class CourseList(admin.ModelAdmin):
    list_display = ('id', 'course_name', 'professor', 'program', 'course_type', 'credits')
    list_filter = ('course_name', 'professor')
    search_fields = ('course_name', 'professor')
    ordering = ['course_name']

class EnrollmentList(admin.ModelAdmin):
    list_display = ('id', 'student','course', 'semester_name', 'start_date', 'end_date', 'status', 'grade')
    list_filter = ('student','course', 'semester_name',)
    search_fields = ('student','course', 'semester_name',)
    ordering = ['student']


admin.site.register(Student, StudentList)
admin.site.register(Course, CourseList)
admin.site.register(Enrollment, EnrollmentList)
