from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models.tag import Tag
from .models.task import Task

admin.site.register(User, UserAdmin)


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")


@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(User, site=task_manager_admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role")
    search_fields = ("username", "email", "first_name", "last_name")
