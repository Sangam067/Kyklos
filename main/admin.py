from django.contrib import admin
from .models import Student, Hostel, Warden, Discussion, Resource, Complaint


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'location')
    list_per_page = 25


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'interest', 'hostel', 'credit_score')
    list_display_links = ('id', 'username')
    list_filter = ('interest', 'hostel')
    search_fields = ('username', 'email')
    list_per_page = 25
    empty_value_display = '—'


@admin.register(Warden)
class WardenAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'hostel', 'gmail')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'gmail')
    list_per_page = 25


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'topic', 'category', 'username')
    list_display_links = ('id', 'title')
    list_filter = ('topic', 'category')
    search_fields = ('title', 'content', 'username')
    list_per_page = 25


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'username')
    list_display_links = ('id', 'title')
    list_filter = ('category',)
    search_fields = ('title', 'username')
    list_per_page = 25


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'studentname', 'roomno', 'priority', 'complaint_type', 'hostelid', 'created_at')
    list_display_links = ('id', 'studentname')
    list_filter = ('priority', 'complaint_type', 'hostelid', 'created_at')
    search_fields = ('studentname', 'roomno', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 25
