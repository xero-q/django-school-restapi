# Generated by Django 5.1.1 on 2024-09-22 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_alter_groupmodel_table_alter_studentmodel_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Subject Name')),
            ],
            options={
                'db_table': 'subject',
            },
        ),
        migrations.CreateModel(
            name='ExamModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Score')),
                ('date', models.DateField(verbose_name='Exam Date')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='school.studentmodel')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='school.subjectmodel')),
            ],
        ),
    ]