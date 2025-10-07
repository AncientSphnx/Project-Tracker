from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . import models


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')

    # Add role to the fieldsets
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'profile_picture', 'mentor', 'progress')}),
    )

    # Add role to the add fieldsets for user creation
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'profile_picture')}),
    )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])  # Hash the password
        super().save_model(request, obj, form, change)


# Register the User model with custom admin
admin.site.register(models.User, CustomUserAdmin)

# Register other models
admin.site.register(models.users_table)
admin.site.register(models.Project)
admin.site.register(models.Task)
admin.site.register(models.Resource)
admin.site.register(models.Updates)
admin.site.register(models.Phases)
admin.site.register(models.MentorStudentAllocation)
