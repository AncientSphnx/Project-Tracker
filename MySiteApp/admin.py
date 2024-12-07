from django.contrib import admin
from .models import User, Project, Updates, Phases

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Updates)
admin.site.register(Phases)