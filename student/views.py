from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)
from rest_framework.response import Response
from .serializers import StudentSerializer, EnrollmentSerializer
from .models import Student, Enrollment, Course
from .serializers import StudentSerializer, CourseSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny,IsAdminUser
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, IsAdminUser))
def getStudent(request, pk):
    """
    Retrieve, update or delete a student instance.
    """
    try:
        student = Student.objects.get(nuid=pk)

    except Student.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student, context={'request': request})
        return Response({'data': serializer.data})

    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def getEnrollment(request, pk):
    """
    Retrieve, update or delete a Enrollment instance.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    try:
        enrollment = Enrollment.objects.get(pk=pk)

    except Enrollment.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EnrollmentSerializer(enrollment, context={'request': request})
        return Response({'data': serializer.data})

    elif request.method == 'PUT':
        serializer = EnrollmentSerializer(enrollment, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        enrollment.delete()
        return Response(status=HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, IsAdminUser))
def enrollment_list(request):
    permission_classes = [IsAuthenticated, IsAdminUser]
    if request.method == 'GET':
        enrollments = Enrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, context={'request': request}, many=True)
        return Response({'data': serializer.data})

    elif request.method == 'POST':
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,IsAdminUser))
def getCourses(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)

    enrollments = Enrollment.objects.filter(student = student).values('course_id')
    courses = Course.objects.exclude(id__in = enrollments).all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)
