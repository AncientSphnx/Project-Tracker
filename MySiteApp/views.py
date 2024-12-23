
from django.shortcuts import render, redirect,get_object_or_404
from datetime import date, timedelta
from django.db import transaction  # For atomic operations
from django.http import JsonResponse
from django.http import HttpResponseForbidden
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from . import models

# Registration View
def register_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user with a hashed password
            user = form.save(commit=False)
            #if not user.role:
            #    user.role = 'student'
            user.save()

            # Authenticate and log in the user
            authenticated_user = authenticate(
                username=user.username,
                password=form.cleaned_data['password1']
            )
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request, "Registration successful!")
                return redirect('login')  # Redirect to a suitable page
            else:
                messages.error(request, "Error during login. Please try again.")
        else:
            print("Form is invalid!")  # This will print if the form is invalid
            print(form.errors)  # Print form errors to see why it failed
            messages.error(request, "Registration failed. Please check the details.")
    else:
        form = forms.RegistrationForm()

    return render(request, 'register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                # Redirect to role-based dashboard
                if user.role == 'student':
                    return redirect('student_dashboard')
                elif user.role == 'mentor':
                    return redirect('mentor_dashboard')
                elif user.role == 'admin':
                    return redirect('/admin/')
                else:
                    messages.error(request, "Unauthorized role!")
                    return redirect('login')
        messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = forms.LoginForm()
    return render(request, 'login.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

# Dashboard View (Role-Based Access)
"""@login_required
def dashboard_view(request):
    if request.user.role == 'student':
        return render(request, 'student_dashboard.html')
    elif request.user.role == 'mentor':
        return render(request, 'mentor_dashboard.html')
    elif request.user.role == 'admin':
        return render(request, 'admin_dashboard.html')
    else:
        messages.error(request, "Unauthorized access!")
        return redirect('login')"""
    
@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('access_denied')  # Redirect unauthorized users

    # Fetch allocated mentor for the student
    '''mentor = getattr(request.user, 'mentor', None)
    if not mentor:
        messages.error(request, "You are not assigned to a mentor.")
        return redirect('profile')  # Redirect to profile or an error page'''
    mentor = request.user.mentor
    # Fetch related data
    accessible_resources = models.Resource.objects.filter(students=request.user)
    allocated_projects = models.Project.objects.filter(students__in=[request.user])
    files_sent_to_mentor = models.Resource.objects.filter(students=request.user, mentor=mentor)

    if request.method == 'POST':
        form = forms.ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)  # Create the object but don't save yet
            resource.mentor = mentor  # Automatically assign the student's mentor
            resource.save()  # Save the object to the database
            resource.students.add(request.user)  # Link the resource to the current student
            return redirect('student_dashboard')  # Refresh the page after form submission
        else:
            print(form.errors)  # Debug form errors if needed
    else:
        form = forms.ResourceForm()

    return render(
        request,
        'dashboards/student_dashboard.html',
        {
            'allocated_projects': allocated_projects,
            'accessible_resources': accessible_resources,
            'files_sent_to_mentor': files_sent_to_mentor,
            'form': form,
        },
    )

@login_required
def mentor_dashboard(request):
    if request.user.role != 'mentor':
        return redirect('access_denied')  # Redirect unauthorized users
    projects = models.Project.objects.filter(mentor=request.user)
    today = date.today()
    upcoming_deadlines = projects.filter(due_date__range=(today, today + timedelta(days=7)))
    if request.method == 'POST':
        form = forms.ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.mentor = request.user  # Assign the logged-in mentor
            if not resource.mentor:
                form.add_error(None, "A mentor must be assigned to this resource.")
            else:
                resource.save()
                form.save_m2m()  # Save Many-to-Many relationships
                return redirect('mentor_dashboard')  # Refresh the page after upload
    else:
        form = forms.ResourceForm()

    calendar_events = [
        {
            "title": project.title,
            "start": str(project.due_date),
            "end": str(project.due_date),
            "description": project.description,
        }
        for project in projects
    ]

    project_data = []
    for project in projects:
        project.allocated_students = project.allocated_students()
        completion_percentage = project.completion_percentage()
        project_data.append({
            'project': project,
            'title': project.title,
            'upcoming_deadlines': upcoming_deadlines,
            'allocated_students': models.Project.allocated_students,
            'completion_percentage': completion_percentage,
            'calendar_events': calendar_events,
        })
    uploaded_resources = models.Resource.objects.filter(mentor=request.user)
    allocated_students = request.user.students.all()  # Assuming `students` is a reverse relation on mentor
    student_documents = models.Resource.objects.filter(students__in=allocated_students).distinct()
    return render(request, 'dashboards/mentor_dashboard.html', {'project_data': project_data,'user': request.user,'form': form,
        'uploaded_resources': uploaded_resources,'student_documents': student_documents})

@login_required
def calendar_events_api(request):
    projects = models.Project.objects.filter(mentor=request.user)
    calendar_events = [
        {
            "title": project.title,
            "start": str(project.due_date),
            "end": str(project.due_date),
            "description": project.description,
        }
        for project in projects
    ]
    return JsonResponse(calendar_events, safe=False)

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('access_denied')  # Redirect unauthorized users
    return render(request, 'dashboards/admin_dashboard.html')

def access_denied(request):
    return render(request, 'access_denied.html', status=403)

@login_required
def profile_view(request):
    user = request.user  # Get the currently logged-in user
    if request.method == 'POST':
        form = forms.ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')  # Redirect back to the profile page
        else:
            messages.error(request, "There was an error updating your profile.")
    else:
        form = forms.ProfileUpdateForm(instance=user)  # Pre-fill form with current user data
    return render(request, 'profile.html', {'form': form})

@login_required
def create_project(request):
    if request.method == "POST":
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('student_dashboard')  # Replace with the appropriate route
    else:
        form = forms.ProjectForm()
    return render(request, 'projects/create_project.html', {'form': form})

@login_required
def delete_project(request, project_id):
    # Fetch the project
    project = get_object_or_404(models.Project, id=project_id, owner=request.user)  # Ensure only the owner can delete it
    if request.method == 'POST':
        project.delete()  # Delete the project
        messages.success(request, "Project deleted successfully!")
        return redirect('all_projects')  # Redirect to the list of all projects
    return render(request, 'projects/confirm_delete.html', {'project': project})



@login_required
def project_details(request, project_id):
    project = get_object_or_404(models.Project, id=project_id)
    phases = project.phases.all()
    return render(request, 'projects/project_details.html', {'project': project, 'phases': phases})


@login_required
def create_phase(request, project_id):
    project = get_object_or_404(models.Project, id=project_id)
    '''TaskFormSet = inlineformset_factory(
        models.Phases,  # Parent model
        models.Task,    # Related model
        fields=('title', 'description', 'due_date', 'status'),  # Fields to include in the formset
        extra=1,  # Number of empty forms to display
        can_delete=True,  # Allow task deletion
    )'''

    if request.method == "POST":
        form = forms.PhaseForm(request.POST)
        #task_formset = forms.TaskFormSet(request.POST)
        if form.is_valid(): #and task_formset.is_valid():
            phase = form.save(commit=False)
            phase.project = project
            phase.save()
            '''tasks = task_formset.save(commit=False)
            for task in tasks:
                task.phase = phase  # Link task to the phase
                task.save()
            task_formset.save_m2m()  # Save any many-to-many relationships'''

            messages.success(request, "Phase and tasks created successfully!")
            return redirect('project_details', project_id=project_id)
    else:
        form = forms.PhaseForm()
        #task_formset = TaskFormSet()
    return render(request, 'phases/create_phase.html', {'form': form,'project': project})#'task_formset': task_formset, 



'''@login_required
def create_task(request, phase_id):
    # Get the phase to which the task will be added
    phase = get_object_or_404(models.Phases, id=phase_id)
    
    if request.method == "POST":
        # Bind the form with data from the request
        form = models.TaskForm(request.POST)
        
        if form.is_valid():
            # Create a new task but link it to the current phase
            task = form.save(commit=False)
            task.phase = phase  # Link the task to the current phase
            task.save()
            
            # Redirect to the phase details page after task is added
            return redirect('phase_details', phase_id=phase.id)  # Update this to your phase detail view name
    else:
        # Initialize the form if it's a GET request
        form = models.TaskForm()

    return render(request, 'projects/create_task.html', {'form': form, 'phase': phase})'''


@login_required
def create_update(request, phase_id):
    phase = get_object_or_404(models.Phases, id=phase_id)
    project = phase.project  # Get the project linked to the phase

    if request.method == "POST":
        # Handle the PhaseForm for updating the phase
        phase_form = forms.PhaseForm(request.POST, instance=phase)
        
        # Handle TaskFormset for adding or updating tasks
        task_formset = forms.TaskFormSet(request.POST)
        
        if phase_form.is_valid() and task_formset.is_valid():
            with transaction.atomic():
                # Save phase
                phase_form.save()

                # Save tasks
                tasks = task_formset.save(commit=False)
                for task in tasks:
                    task.phase = phase
                    task.save()

                # Delete tasks marked for deletion
                for deleted_task in task_formset.deleted_objects:
                    deleted_task.delete()

            return redirect('project_details', project_id=project.id)
        else:
            print("Phase Form Errors:", phase_form.errors)
            print("Task Formset Errors:", task_formset.errors)
        
    else:
        phase_form = forms.PhaseForm(instance=phase)
        task_formset = forms.TaskFormSet(queryset=models.Task.objects.filter(phase=phase))  # Get tasks associated with the phase

    return render(request, 'phases/create_update.html', {'phase_form': phase_form,'task_formset': task_formset,'phase': phase})

@login_required
def update_tasks(request, phase_id):
    phase = get_object_or_404(models.Phases, id=phase_id)

    # Initialize TaskFormSet with tasks linked to the phase
    task_formset = forms.TaskFormSet(
        request.POST or None, queryset=models.Task.objects.filter(phase=phase)
    )

    if request.method == "POST":
        if task_formset.is_valid():
            # Save updated tasks
            tasks = task_formset.save(commit=False)
            for task in tasks:
                task.save()

            # Handle deleted tasks if `can_delete=True`
            for deleted_task in task_formset.deleted_objects:
                deleted_task.delete()

            return redirect('project_details', project_id=phase.project.id)
        else:
            print("Task Formset Errors:", task_formset.errors)

    return render(request, 'projects/update_task.html', {
        'task_formset': task_formset,
        'phase': phase,
    })

@login_required
def phase_details(request, phase_id):
    # Fetch the phase using the phase_id
    phase = get_object_or_404(models.Phases, id=phase_id)

    # Fetch the tasks related to this phase
    tasks = phase.tasks.all()

    # Render the details of the phase and its tasks
    return render(request, 'phases/phase_details.html', {'phase': phase, 'tasks': tasks})

def delete_phase(request, phase_id):
    phase = get_object_or_404(models.Phases, id=phase_id)
    project_id = phase.project.id
    if request.method == 'POST':
        phase.delete()
        return redirect('project_details', project_id=project_id)
    return render(request, 'phases/confirm_delete.html', {'phase': phase})

@login_required
def all_projects(request):
    # Get all the projects for the logged-in user
    projects = models.Project.objects.filter(owner=request.user)
    
    return render(request, 'projects/all_projects.html', {'projects': projects})

@login_required
def progress_tracker(request):
    projects = models.Project.objects.filter(owner=request.user)

    # For each project, calculate completion progress
    for project in projects:
        total_phases = project.phases.count()
        completed_phases = project.phases.filter(status='completed').count()
        project.completion_percentage = (completed_phases / total_phases) * 100 if total_phases > 0 else 0

        # For each phase, calculate completion progress based on tasks
        for phase in project.phases.all():
            total_tasks = phase.tasks.count()
            completed_tasks = phase.tasks.filter(status='completed').count()
            phase.completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

            # For each task, calculate completion progress
            for task in phase.tasks.all():
                task.completion_percentage = 100 if task.status == 'completed' else 0

    return render(request, 'progress_tracker.html', {'projects': projects})



@login_required
def allocated_students_view(request):
    # Ensure the user is a mentor
    if request.user.role != 'mentor':
        return redirect('access_denied')

    # Get all projects supervised by the mentor
    #mentor_projects = models.Project.objects.filter(mentor=request.user)

    # Get unique students assigned to the mentor's projects
    allocated_students = models.User.objects.filter(
        id__in=models.MentorStudentAllocation.objects.filter(mentor=request.user).values('student_id')
    )

    return render(request, 'mentor/allocated_students.html', {
        'students': allocated_students,
    })


@login_required
def mentor_student_projects(request):
    if request.user.role != 'mentor':
        return redirect('access_denied')  # Redirect unauthorized users
    
    # Get the logged-in mentor
    mentor = request.user

    # Get all students allocated to the logged-in mentor
    allocated_students = models.User.objects.filter(
        id__in=models.MentorStudentAllocation.objects.filter(mentor=mentor).values('student_id')
    )
    
    # If no students are allocated to the mentor, return an empty response or a message
    if not allocated_students:
        return render(request, 'mentor/all_projects.html', {'message': 'No students allocated to you yet.'})
    
    # Get all projects that the allocated students are working on
    student_projects = models.Project.objects.filter(
        students__in=allocated_students
    ).distinct()  # Use distinct to avoid duplicates in case multiple students are on the same project

    # If no projects are found for the allocated students, show a message
    if not student_projects:
        return render(request, 'mentor/all_projects.html', {'message': 'No projects found for your students.'})

    # Render the template with the student projects
    return render(request, 'mentor/all_projects.html', {'student_projects': student_projects})

@login_required
def project_detail_mentor(request, project_id):
    # Ensure that the user is a mentor (or any other role check you need)
    if request.user.role != 'mentor':
        return redirect('access_denied')  # Redirect unauthorized users

    # Get the project by its ID
    project = get_object_or_404(models.Project, id=project_id)

    # Render the project details template
    return render(request, 'mentor/project_details_mentor.html', {'project': project})

@login_required
def upload_resource(request):
    if request.method == 'POST':
        form = forms.ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.mentor = request.user  # Assign the logged-in mentor
            resource.save()
            form.save_m2m()  # Save Many-to-Many relationships
            return redirect('mentor_dashboard')  # Redirect to the dashboard
    else:
        form = forms.ResourceForm()
    return render(request, 'mentor/upload_resource.html', {'form': form})

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = forms.ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.student = request.user
            document.mentor = request.user.profile.assigned_mentor  # Replace with your logic for mentor assignment
            document.save()
            return redirect('student_dashboard')  # Replace with the name of your student dashboard URL
    else:
        form = forms.ResourceForm()
    return render(request, 'upload_document.html', {'form': form})

@login_required
def delete_resource(request, resource_id):
    resource = get_object_or_404(models.Resource, id=resource_id)

    # Ensure only assigned students or mentors can delete the resource
    if request.user == resource.mentor or request.user in resource.students.all():
        resource.delete()
        return redirect('student_dashboard')  # Replace with the name of your dashboard URL
    else:
        return HttpResponseForbidden("You don't have permission to delete this resource.")


def index(request):
     return render(request, 'index.html')

"""def user_form_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Process the form data
            
            user = User1(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                role=form.cleaned_data['role']
            )
            user.save()
            
            # Here you can save data to the database or perform other actions
            #return HttpResponse(f"Thank you, {user.name}. Your information has been submitted!")
            return redirect('index')
        
    else:
        form = UserForm()

    return render(request, 'user_form.html', {'form': form})

def user_list_view(request):
    users = User1.objects.all()  # Get all user records from the User table
    return render(request, 'user_list.html', {'users': users})"""