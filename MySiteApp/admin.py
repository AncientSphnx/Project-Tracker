from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import  models

'''@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')'''

class CustomUserAdmin(UserAdmin):
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])  # Hash the password
        super().save_model(request, obj, form, change)




admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.users_table)
#admin.site.register(models.Project)
@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'mentor', 'start_date', 'due_date')
    filter_horizontal = ('students',)  
admin.site.register(models.Task)
admin.site.register(models.Updates)
admin.site.register(models.Phases)
admin.site.register(models.MentorStudentAllocation)



