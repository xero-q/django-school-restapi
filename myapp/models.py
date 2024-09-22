from django.db import models
from django.core.exceptions import ValidationError
import phonenumbers

# Create your models here.
def validate_phone_number(value):
    try:
        phone_number = phonenumbers.parse(value, None)  # Assuming international format
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError(f'{value} is not a valid phone number.')
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError(f'{value} is not a valid phone number.')

class PersonModel(models.Model):
    name=models.CharField(max_length=200, verbose_name='Name')
    dob=models.DateField(verbose_name='Birth Date')
    sex=models.CharField(max_length=1, verbose_name='Sex')
    address=models.CharField(max_length=255, null=True, verbose_name='Address')
    phone=models.CharField(max_length=20,null=True,verbose_name='Phone number', validators=[validate_phone_number])

    def __str__(self):
        return self.name
    
class GroupModel(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Name')

    class Meta:
        db_table = 'group'  
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def get_groups_with_student_count():
        return GroupModel.objects.annotate(student_count=models.Count('students')).order_by('-student_count')
    
    @staticmethod
    def get_groups_with_average_score(after_date):
        from django.db.models import Avg
        from django.db.models import Q

        return GroupModel.objects.annotate(
            average_score=Avg('students__exams__score', filter=Q(students__exams__date__gt=after_date))
        ).order_by('-average_score')
    
class StudentModel(models.Model):
    name=models.CharField(max_length=255, verbose_name='Name')
    phone=models.CharField(max_length=20,unique=True, verbose_name='Phone Number',validators=[validate_phone_number] )
    group=models.ForeignKey(GroupModel, on_delete=models.CASCADE, related_name='students')

    class Meta:
        db_table = 'student'  
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def top_scoring_student_by_group(group_id):
        top_student = StudentModel.objects.filter(group=group_id) \
                                  .annotate(average_score=models.Avg('exams__score')) \
                                  .order_by('-average_score') \
                                  .first()
        
        return top_student
    
class SubjectModel(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Subject Name')

    class Meta:
        db_table = 'subject'

    def __str__(self):
        return self.name


class ExamModel(models.Model):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey(SubjectModel, on_delete=models.CASCADE, related_name='exams')
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Score')
    date = models.DateField(verbose_name='Exam Date')

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.score})"
    

