from django.contrib import admin
# from django.contrib.auth.models import User
from .models import *


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(About)
class AboutAdmin(SingletonAdmin):
    list_display = ['content_message', 'profile_picture']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'qualification', 'year_month', 'description')
    search_fields = ('school_name', 'qualification')
    list_filter = ('school_name', 'qualification', 'year_month')


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'position', 'start_date', 'end_date', 'description')
    search_fields = ('company_name', 'position')
    list_filter = ('company_name', 'position', 'start_date', 'end_date')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'client', 'summery', 'description', 'project_banner_image',  'project_url')
    search_fields = ('project_name', 'client')
    list_filter = ('project_name', 'client')


@admin.register(Contact)
class ContactAdmin(SingletonAdmin):
    list_display = ('contact', 'email', 'facebook_link', 'X_link', 'linked_in', 'address')
    search_fields = ('contact', 'email')
    list_filter = ('contact', 'email')


@admin.register(SystemInfo)
class SystemInfoAdmin(SingletonAdmin):
    list_display = ('system_name', 'system_short_name', 'owner_name', 'welcome_message', 'system_logo', 'background_image')
    search_fields = ('system_name', 'system_short_name')
    list_filter = ('system_name', 'system_short_name')


@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'testimony', 'background_image')
    search_fields = ['client_name']
    list_filter = ('client_name', 'testimony')