from django.urls import path
from .views import (
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
]
