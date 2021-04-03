from rest_framework import serializers
from .models import Student, Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ('pk', 'semester_name', 'start_date', 'end_date', 'status', 'grade')


class StudentSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(many=True)
    enrollments = serializers.SerializerMethodField('get_enrollments')

    def get_enrollments(self, student):
        enrollments = Enrollment.objects.filter(student=student).values()
        print(enrollments)
        return enrollments

    class Meta:
        model = Student
        fields = ('pk', 'name', 'email', 'cell_phone', 'start_date', 'graduation_date', 'enrollments')
