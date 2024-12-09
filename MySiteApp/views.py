
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm,LoginForm
from .models import User

# Registration View
def register_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = RegistrationForm(request.POST)
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
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
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
        form = LoginForm()
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
    return render(request, 'dashboards/student_dashboard.html')

@login_required
def mentor_dashboard(request):
    if request.user.role != 'mentor':
        return redirect('access_denied')  # Redirect unauthorized users
    return render(request, 'dashboards/mentor_dashboard.html')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('access_denied')  # Redirect unauthorized users
    return render(request, 'dashboards/admin_dashboard.html')

def access_denied(request):
    return render(request, 'access_denied.html', status=403)



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