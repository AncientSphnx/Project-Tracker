# Generated by Django 5.1.3 on 2024-12-12 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MySiteApp', '0007_project_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='status',
        ),
    ]
