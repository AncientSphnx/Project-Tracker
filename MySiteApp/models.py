from django.db import models

from django.db import models

# User Table
class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    email = models.EmailField(unique=True)       # Ensures unique emails
    role = models.CharField(max_length=50)       # Role of the user
    name = models.CharField(max_length=100)      # Name of the user

    def __str__(self):
        return self.name

# Project Table
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User table

    def __str__(self):
        return self.title

# Updates Table
class Updates(models.Model):
    update_id = models.AutoField(primary_key=True)
    resources = models.TextField()
    comments = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # Link to Project table

    def __str__(self):
        return f"Update {self.update_id} for Project {self.project.title}"

# Phases Table
class Phases(models.Model):
    p_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50)
    due_date = models.DateField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # Link to Project table

    def __str__(self):
        return f"Phase {self.p_id} for Project {self.project.title}"
