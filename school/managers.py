from django.db import models

class StudentScoreManager(models.Manager):
    def get_queryset(self):
        # Return a queryset for the view
        return super().get_queryset()