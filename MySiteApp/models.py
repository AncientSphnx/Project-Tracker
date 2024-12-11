from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('mentor', 'Mentor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    id = models.AutoField(primary_key=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    def __str__(self):
        return f"{self.username} ({self.role})"

# User Table
class users_table(models.Model):
    user_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    email = models.EmailField(unique=True)       # Ensures unique emails
    role = models.CharField(max_length=50)       # Role of the user
    name = models.CharField(max_length=100)      # Name of the user

    def __str__(self):
        return self.name

# Project Table
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    due_date = models.DateField(default="2024-12-31")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.title


class Phases(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,default="Default Phase Title")
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='phases')

    def __str__(self):
        return f"Phase: {self.title} ({self.project.title})"


class Updates(models.Model):
    resources = models.TextField()
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    phase = models.ForeignKey(Phases, on_delete=models.CASCADE, related_name='updates',default=1)

    def __str__(self):
        return f"Update {self.pk} for Phase {self.phase.title}"
