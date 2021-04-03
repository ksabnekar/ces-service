from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)
from rest_framework.response import Response
from .models import Student, Enrollment
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny,IsAdminUser
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def getStudent(request, pk):
    """
    Retrieve, update or delete a student instance.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
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
