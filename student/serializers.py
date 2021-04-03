from rest_framework import serializers
from .models import Student, Enrollment, Course


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
        for enrollemnt in enrollments:
            courseid =  Course.objects.filter(id = enrollemnt['course_id']).values('course_id', 'course_name')
            for c in courseid:
                enrollemnt['course_id'] = c['course_id'] + '-' + c['course_name']
            print(courseid)
        print(enrollments)
        return enrollments

    class Meta:
        model = Student
        fields = ('pk', 'name', 'nuid',  'email', 'cell_phone', 'start_date', 'graduation_date', 'enrollments')
