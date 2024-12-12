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
    mentor = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='students'
    )  # Link students to mentors
    progress = models.FloatField(default=0.0) 
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects',null=True, blank=True)
    mentor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mentored_projects')  # Supervisor (mentor)
    students = models.ManyToManyField(
        User, related_name='assigned_projects', blank=True, limit_choices_to={'role': 'student'}
    )

    def allocated_students(self):
        return User.objects.filter(
            mentor=self.mentor, 
            role='student', 
            id__in=MentorStudentAllocation.objects.filter(mentor=self.mentor).values('student_id')
        )

    
    
    
    def completion_percentage(self):
        # Calculate project completion based on phases completion
        phases = self.phases.all()
        total_phases = phases.count()
        if total_phases == 0:
            return 0
        completed_phases = sum(phase.completion_percentage() for phase in phases)
        return (completed_phases / total_phases)
    
    def __str__(self):
        return self.title



class Phases(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,default="Default Phase Title")
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='phases')
    mentor_notes = models.TextField(blank=True, null=True)  # Notes from the mentor

    
    
    
    def completion_percentage(self):
        # Calculate phase completion based on tasks completion
        tasks = self.tasks.all()
        total_tasks = tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = sum(1 for task in tasks if task.status == 'completed')
        return (completed_tasks / total_tasks) * 100
    
    def __str__(self):
        return f"Phase: {self.title} ({self.project.title})"

    
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    phase = models.ForeignKey('Phases', on_delete=models.CASCADE, related_name='tasks')  # link to a phase

    def completion_percentage(self):
        # This can be a fixed value (100 for completed, 0 for others)
        return 100 if self.status == 'completed' else 0

    def __str__(self):
        return f"Task: {self.title} ({self.phase.title})"


class Updates(models.Model):
    resources = models.TextField()
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    phase = models.ForeignKey(Phases, on_delete=models.CASCADE, related_name='updates',default=1)
    shared_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='shared_updates')  # Track who shared the update

    def __str__(self):
        return f"Update {self.pk} for Phase {self.phase.title}"

class MentorStudentAllocation(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='allocated_students')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentors')
    allocated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mentor', 'student')  # Ensure a mentor-student pair is unique

    def __str__(self):
        return f"{self.mentor.username} -> {self.student.username}"