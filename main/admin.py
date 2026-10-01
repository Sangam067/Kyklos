from django.contrib import admin
from .models import Student, Hostel, Warden, Discussion, Resource, Complaint


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')
    search_fields = ('name', 'location')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'interest', 'hostel', 'credit_score')
    list_filter = ('interest', 'hostel')
    search_fields = ('username', 'email')


@admin.register(Warden)
class WardenAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'hostel', 'gmail')
    search_fields = ('username', 'gmail')


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'topic', 'category', 'username')
    list_filter = ('topic', 'category')
    search_fields = ('title', 'content', 'username')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'username')
    list_filter = ('category',)
    search_fields = ('title', 'username')


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'studentname', 'roomno', 'priority', 'complaint_type', 'hostelid', 'created_at')
    list_filter = ('priority', 'complaint_type', 'hostelid', 'created_at')
    search_fields = ('studentname', 'roomno', 'description')
