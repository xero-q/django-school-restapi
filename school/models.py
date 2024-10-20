from django.db import models
from django.core.exceptions import ValidationError
import phonenumbers
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models import Q

from .managers import StudentScoreManager

# Create your models here.
def validate_phone_number(value):
    """
    Validates a given phone number

    Args
        value (str): The phone number
    """
    try:
        phone_number = phonenumbers.parse(value, None)  # Assuming international format
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError(f"{value} is not a valid phone number.")
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError(f"{value} is not a valid phone number.")


class GroupModel(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")

    class Meta:
        db_table = "group"

    def __str__(self):
        return self.name

    @staticmethod
    def get_groups_with_student_count():
        """
        Returns all groups with the amount of students each one has
        """
        return GroupModel.objects.annotate(
            student_count=models.Count("students")
        ).order_by("-student_count")


class StudentModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    phone = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Phone Number",
        validators=[validate_phone_number],
    )
    group = models.ForeignKey(
        GroupModel, on_delete=models.CASCADE, related_name="students"
    )

    class Meta:
        db_table = "student"

    def __str__(self):
        return f"{self.name} ({self.group.name})"

    @staticmethod
    def top_scoring_student_by_group(group_id):
        """
        Returns the student with the top average score for a given group

        Args
            group_id (int): The ID of the group
        """
        top_student = (
            StudentModel.objects.filter(group=group_id)
            .annotate(average_score=models.Avg("exams__score"))
            .order_by("-average_score")
            .first()
        )

        return top_student


class SubjectModel(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Subject Name")

    class Meta:
        db_table = "subject"

    def __str__(self):
        return self.name


class ExamType(models.TextChoices):
    partial = "Partial"
    final = "Final"


class ExamModel(models.Model):
    student = models.ForeignKey(
        StudentModel, on_delete=models.CASCADE, related_name="exams"
    )
    subject = models.ForeignKey(
        SubjectModel, on_delete=models.CASCADE, related_name="exams"
    )
    score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Score")
    type = models.CharField(max_length=200, choices=ExamType, default=ExamType.partial)
    date = models.DateField(verbose_name="Exam Date")

    def __str__(self):
        return f"{self.student.name} ({self.student.group.name}) - {self.subject} ({self.score})"

    class Meta:
        db_table = "exam"

    @staticmethod
    def list_exams_students_subjects():
        return (
            ExamModel.objects.all()
            .annotate(
                student_name=F("student__name"),
                subject_name=F("subject__name"),
                group=F("student__group__name"),
            )
            .values("student_name", "subject_name", "group")
            .order_by("student_name")
        )


class UserModel(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    email = models.CharField(max_length=100, unique=True, verbose_name="Email")
    birthdate = models.DateField(verbose_name="Date of Birth")
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Phone Number",
        validators=[validate_phone_number],
    )

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class PersonModel(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    dob = models.DateField(verbose_name="Date of Birth")
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
        error_messages={
            "unique": "This email address is already in use.",
            "invalid": "The email is invalid.",
        },
    )  

    class Meta:
        db_table = "people"

    @staticmethod
    def get_by_name_email(name, email):
        return PersonModel.objects.filter(Q(name__icontains=name) & Q(email__icontains=email))

class StudentAverageScore(models.Model):
    student_name = models.CharField(max_length=255, primary_key=True)
    group_name = models.CharField(max_length=255)
    average_score = models.DecimalField(max_digits=5, decimal_places=2)

    objects = StudentScoreManager()

    class Meta:
        # Tell Django not to create a table for this model
        managed = False
        # Name of the database view
        db_table = 'students_average_score'
