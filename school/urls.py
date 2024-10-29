from django.http import JsonResponse
from django.urls import path, include
from .views import (
    process_detail,
    user_form_view,
    StudentRetrieveUpdateDestroyView,
    GroupListCreateView,
    StudentListCreateView,
    GroupRetrieveUpdateDestroView,
    SubjectListCreateView,
    ExamListCreateView,
    ExamRetrieveUpdateDestroyView,
    SubjectRetrieveUpdateDestroyView,
    students_by_group,
    top_student_by_group,
    ProcessGetPost,
    price_coin,
    DownloadPeopleExcel,
    user_data,
    StudentAverageScoreList
)

urlpatterns = [
    path("api/group", GroupListCreateView.as_view(), name="group-create-list"),
    path(
        "api/group/<int:pk>",
        GroupRetrieveUpdateDestroView.as_view(),
        name="group-update-delete-retrieve",
    ),
    path("api/group/count", students_by_group, name="group-students-count"),
    path(
        "api/group/top-student/<int:group_id>",
        top_student_by_group,
        name="group-top-student",
    ),
    path("api/student", StudentListCreateView.as_view(), name="student-create-list"),
    path(
        "api/student/<int:pk>",
        StudentRetrieveUpdateDestroyView.as_view(),
        name="student-update-delete-retrieve",
    ),
    path("api/subject", SubjectListCreateView.as_view(), name="subject-create-list"),
    path(
        "api/subject/<int:pk>",
        SubjectRetrieveUpdateDestroyView.as_view(),
        name="subject-update-delete-retrieve",
    ),
    path("api/exam", ExamListCreateView.as_view(), name="exam-create-list"),
    path(
        "api/exam/<int:pk>",
        ExamRetrieveUpdateDestroyView.as_view(),
        name="exam-update-delete-retrieve",
    ),
    path("user", user_form_view, name="user-form"),
    path("people/excel",DownloadPeopleExcel.as_view(),name="download-excel"),
    path("process", ProcessGetPost.as_view(), name="process"),
    path("process/<int:pk>", process_detail, name="process-detail"),
    path("price/<str:coin>", price_coin,name='price-coin'),
    path('data-list',user_data, name="People List"),
    path('students-score',StudentAverageScoreList.as_view(),name='student-score')
]
