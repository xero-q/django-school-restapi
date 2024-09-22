from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import GroupModel, StudentModel, SubjectModel, ExamModel
from .serializers import GroupModelSerializer, \
                  StudentModelSerializer, SubjectModelSerializer,ExamModelSerializer
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

class GroupListCreateView(generics.ListCreateAPIView):
    queryset = GroupModel.objects.all()
    serializer_class = GroupModelSerializer   

class GroupRetrieveUpdateDestroView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupModel.objects.all()
    serializer_class = GroupModelSerializer   

class StudentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'perPage'
    max_page_size = 100

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = StudentModel.objects.all()
    serializer_class = StudentModelSerializer   
    pagination_class=StudentPagination

class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentModel.objects.prefetch_related('exams')
    serializer_class = StudentModelSerializer   

class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = SubjectModel.objects.all()
    serializer_class = SubjectModelSerializer   


class ExamListCreateView(generics.ListCreateAPIView):
    queryset = ExamModel.objects.all()
    serializer_class = ExamModelSerializer     

@api_view()
def students_by_group(request):
    groups = GroupModel.get_groups_with_student_count()

    data = [{'group_name':group.name, 'student_count':group.student_count} for group in groups]

    return Response(data,status=status.HTTP_200_OK)

@api_view()
def average_by_group(request, date):
    groups = GroupModel.get_groups_with_average_score(date)

    print(groups)

    data = [{'group_name':group.name, 'average_score':group.average_score} for group in groups]

    return Response(data,status=status.HTTP_200_OK)


@api_view()
def top_student_by_group(request, group_id):
    student = StudentModel.top_scoring_student_by_group(group_id)

    if not student:
        return Response({"message":"No student found"},status=status.HTTP_404_NOT_FOUND)

    serialized_data = StudentModelSerializer(student)

    return Response(serialized_data.data,status=status.HTTP_200_OK)
