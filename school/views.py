from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import (
    GroupModel,
    StudentAverageScore,
    StudentModel,
    SubjectModel,
    ExamModel,
    UserModel,
)
from .serializers import (
    GroupModelSerializer,
    StudentAverageScoreSerializer,
    StudentModelSerializer,
    SubjectModelSerializer,
    ExamModelSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView
from django.db import models
from rest_framework import viewsets
import os
import requests
from django.http import HttpResponse
from openpyxl import Workbook
from datetime import datetime

class GroupListCreateView(generics.ListCreateAPIView):
    queryset = GroupModel.objects.all()
    serializer_class = GroupModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GroupRetrieveUpdateDestroView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupModel.objects.all()
    serializer_class = GroupModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class StudentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "perPage"
    max_page_size = 100


class StudentListCreateView(generics.ListCreateAPIView):
    queryset = StudentModel.objects.prefetch_related("exams")
    serializer_class = StudentModelSerializer
    pagination_class = StudentPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Call the original queryset method to get the base queryset
        queryset = super().get_queryset()
        order_by = self.request.query_params.get("order_by") or "name"
        sort = self.request.query_params.get("sort") or "asc"

        if sort == "desc":
            order_by = f"-{order_by}"

        queryset = queryset.order_by(order_by)

        return queryset


class StudentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentModel.objects.prefetch_related("exams")
    serializer_class = StudentModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = SubjectModel.objects.all()
    serializer_class = SubjectModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SubjectRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubjectModel.objects.all()
    serializer_class = SubjectModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ExamListCreateView(generics.ListCreateAPIView):
    queryset = ExamModel.objects.all()
    serializer_class = ExamModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ExamRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExamModel.objects.all()
    serializer_class = ExamModelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view()
def students_by_group(request):
    """
    Returns all groups with the amount of students each one has.

    """
    groups = GroupModel.get_groups_with_student_count()

    data = [
        {"group_name": group.name, "student_count": group.student_count}
        for group in groups
    ]

    return Response(data, status=status.HTTP_200_OK)


@api_view()
def top_student_by_group(request, group_id):
    """
    Returns the student with the best average score in exams

    Args:
        group_id (int): The ID of the group.
    """
    student = StudentModel.top_scoring_student_by_group(group_id)

    if not student:
        return Response(
            {"message": "No student found"}, status=status.HTTP_404_NOT_FOUND
        )

    serialized_data = StudentModelSerializer(student)

    return Response(serialized_data.data, status=status.HTTP_200_OK)

def home_view(request):
    students = StudentModel.objects.annotate(average_score=models.Avg("exams__score"))

    context = {"students": students}

    return render(request, "home.html", context)


def user_form_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = UserModel(
                full_name=form.cleaned_data["full_name"],
                email=form.cleaned_data["email"],
                birthdate=form.cleaned_data["birthdate"],
                phone_number=form.cleaned_data["phone_number"],
            )
            user.save()
            return render(
                request, "success.html", {"full_name": form.cleaned_data["full_name"]}
            )
    else:
        form = UserForm()
    return render(request, "user_form.html", {"form": form})


def user_data(request):
    people = PersonModel.objects.all().order_by("name")

    return render(request, "data.html", {"people": people})


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def process_detail(request, pk):
    person = get_object_or_404(PersonModel, pk=pk)

    match request.method:
        case "GET":
            serializer = PersonModelSerializer(person)
            return Response(serializer.data)
        case "PUT":
            serializer = PersonModelSerializer(person, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )  # Return errors if validation fails

        case "PATCH":
            serializer = PersonModelSerializer(person, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )  # Return errors if validation fails

        case "DELETE":
            person.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PersonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "perPage"
    max_page_size = 100


class ProcessGetPost(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        order_by = request.query_params.get("order_by") or "name"
        sort = request.query_params.get("sort") or "asc"

        if sort == "desc":
            order_by = f"-{order_by}"

        people = PersonModel.objects.all().order_by(order_by)

        paginator = PersonPagination()

        page = paginator.paginate_queryset(people, request)

        if page is not None:
            serializer = PersonModelSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = PersonModelSerializer(people, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data.update({"user": request.user.id})
        serializer = PersonModelSerializer(data=data)  # Deserialize the incoming data
        if serializer.is_valid():  # Validate the incoming data
            serializer.save()  # Save the valid data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DownloadPeopleExcel(APIView):
    @staticmethod
    def format_dob(person):
        return datetime.strftime(person.dob,'%d-%m-%Y')
    
    
    def get(self, request):
        wb = Workbook()
        ws = wb.active
        ws.title = "Sample Data"   
        
        ws.append(["Name", "Birth Date", "Email"])
        people = PersonModel.objects.all()

        people_data = [[person.name,self.format_dob(person), person.email] for person in people]

        for row in people_data:
            ws.append(row)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # Set the file name in the response
        response['Content-Disposition'] = 'attachment; filename="people.xlsx"'

        # Save the workbook to the response
        wb.save(response)
    
        return response

class StudentAverageScoreList(generics.ListAPIView):
    queryset = StudentAverageScore.objects.all()
    serializer_class = StudentAverageScoreSerializer

def price_coin(request,coin):
    URL = f"https://rest.coinapi.io/v1/exchangerate/{coin}/USD"
    HEADERS = {
                'Accept': 'text/plain',
                 'Authorization':os.getenv('COIN_API_KEY')
              }
                  
    try:
        response = requests.get(url=URL, headers=HEADERS)

        json = response.json()
        if 'rate' in json.keys():
            return JsonResponse({'value':round(json['rate'],2)})        
        else:
            return JsonResponse({'success':False,'message':f'Impossible to get the price of {coin.upper()} at this moment'},status=status.HTTP_503_SERVICE_UNAVAILABLE) 
    except:
        return JsonResponse({'success':False,'message':'There was an error while making the request'},status=status.HTTP_502_BAD_GATEWAY)          
