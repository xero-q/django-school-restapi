# Generated by Django 5.1.1 on 2024-09-22 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("school", "0002_group_student"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Group",
            new_name="GroupModel",
        ),
        migrations.RenameModel(
            old_name="Student",
            new_name="StudentModel",
        ),
    ]
