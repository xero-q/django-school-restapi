from django.contrib import admin
from .models import StudentModel, GroupModel, SubjectModel, ExamModel, PersonModel

admin.site.register(StudentModel)
admin.site.register(GroupModel)
admin.site.register(SubjectModel)
admin.site.register(ExamModel)
admin.site.register(PersonModel)
