from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User

def user_form_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Process the form data
            
            user = User(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                role=form.cleaned_data['role']
            )
            user.save()
            
            # Here you can save data to the database or perform other actions
            return HttpResponse(f"Thank you, {user.name}. Your information has been submitted!")
    else:
        form = UserForm()

    return render(request, 'user_form.html', {'form': form})

def user_list_view(request):
    users = User.objects.all()  # Get all user records from the User table
    return render(request, 'user_list.html', {'users': users})