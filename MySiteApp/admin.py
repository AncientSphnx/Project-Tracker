from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import  models



class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role')
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])  # Hash the password
        super().save_model(request, obj, form, change)

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role')


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'mentor', 'start_date', 'due_date')
    filter_horizontal = ('students',)  


#admin.site.register(models.User, CustomUserAdmin,UserAdmin)
admin.site.register(models.users_table)
#admin.site.register(models.Project)

admin.site.register(models.Task)
admin.site.register(models.Resource)
admin.site.register(models.Updates)
admin.site.register(models.Phases)
admin.site.register(models.MentorStudentAllocation)



