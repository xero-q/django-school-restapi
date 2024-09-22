from django.urls import path, include
from .views import HomeView,PersonListCreateView,StudentRetrieveUpdateDestroyView, PersonRetrieveUpdateDestroyAPIView, GroupListCreateView,StudentListCreateView,GroupRetrieveUpdateDestroView,SubjectListCreateView, ExamListCreateView,students_by_group,average_by_group,hello,top_student_by_group
from rest_framework.routers import DefaultRouter
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema


urlpatterns = [
    path('api/home', HomeView.as_view(), name='home-api'),
     path('api/people', PersonListCreateView.as_view(),name='people-create-list'),
     path('api/people/<int:pk>', PersonRetrieveUpdateDestroyAPIView.as_view(),name='people-retrieve-update-delete'),
     path('api/group', GroupListCreateView.as_view(),name='group-create-list'),
     path('api/group/<int:pk>', GroupRetrieveUpdateDestroView.as_view(),name='group-update-delete-retrieve'),
     path('api/group/count', students_by_group,name='group-students-count'),
     path('api/group/average/<str:date>', average_by_group,name='group-average-score'),
     path('api/group/top-student/<int:group_id>', top_student_by_group,name='group-top-student'),
     path('api/student', StudentListCreateView.as_view(),name='student-create-list'),
     path('api/student/<int:pk>', StudentRetrieveUpdateDestroyView.as_view(),name='student-update-delete-retrieve'),
     path('api/subject', SubjectListCreateView.as_view(),name='subject-create-list'),
     path('api/exam', ExamListCreateView.as_view(),name='exam-create-list'),
     path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
     path('hello/<str:name>',hello,name='hello')
]