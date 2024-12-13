from django import forms
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import models



# Registration Form
class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    class Meta:
        model = models.User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True  # Ensure email is mandatory
        #self.fields['role'].choices = User.ROLE_CHOICES  # Populate role choices dynamically
        #self.fields['role'].initial = 'student'  # Default role to student

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if not self.cleaned_data.get('role'):
            user.role = 'student'  # Default to student if role is not provided
        if commit:
            user.save()
        return user'''


# Login Form
class LoginForm(AuthenticationForm):
    class Meta:
        model = models.User
        fields = ['username', 'password']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'profile_picture']  # Fields to update
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ProjectForm(forms.ModelForm):
    task_title = forms.CharField(max_length=100, required=False, label="Task Title")
    task_description = forms.CharField(widget=forms.Textarea, required=False, label="Task Description")
    task_due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Task Due Date")
    task_status = forms.ChoiceField(choices=[('pending', 'Pending'), ('completed', 'Completed')], required=False, label="Task Status")

    class Meta:
        model = models.Project
        fields = ['title', 'description', 'start_date', 'due_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    

class PhaseForm(forms.ModelForm):
    task_title = forms.CharField(max_length=100, required=False, label="Task Title")
    task_description = forms.CharField(widget=forms.Textarea, required=False, label="Task Description")
    task_due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False, label="Task Due Date")
    task_status = forms.ChoiceField(choices=[('pending', 'Pending'), ('completed', 'Completed')], required=False, label="Task Status")

    class Meta:
        model = models.Phases
        fields = ['title', 'description', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Save the phase first
        phase = super().save(commit=False)
        if commit:
            phase.save()
            

        # If task data is provided, save the task as well
        task_title = self.cleaned_data.get('task_title')
        task_description = self.cleaned_data.get('task_description')
        task_due_date = self.cleaned_data.get('task_due_date')
        task_status = self.cleaned_data.get('task_status')

        if task_title and task_description and task_due_date and task_status:
            
            # Create the task linked to the newly created phase
           task = models.Task.objects.create(
                title=task_title,
                description=task_description,
                due_date=task_due_date,
                status=task_status,
                phase=phase
            )

        return phase

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['title', 'description', 'due_date', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=[('pending', 'Pending'), ('completed', 'Completed')]),
        }

TaskFormSet = modelformset_factory(models.Task, form=TaskForm, extra=1)

class ResourceForm(forms.ModelForm):
    class Meta:
        model = models.Resource
        fields = ['title', 'file', 'description', 'students']




class UpdateForm(forms.ModelForm):
    class Meta:
        model = models.Updates
        fields = ['resources', 'comments']

class UserForm(forms.Form):
    name = forms.CharField(max_length=100, label="Full Name", widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    role = forms.ChoiceField(
        label="Role",
        choices=[('admin', 'Admin'), ('developer', 'Developer'), ('manager', 'Manager'), ('other', 'Other')],
    )
    additional_info = forms.CharField(
        label="Additional Information",
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Enter any additional information (optional)', 'rows': 4}),
    )