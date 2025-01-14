from django.contrib import admin
from .models import (Hostel,Room,Student,Parents,Visitors,Mess,Fees,Staff)


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['hostel_name', 'no_of_rooms', 'no_of_students', 'hostel_type']
    list_filter = ['hostel_type']
    
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'student_phone', 'hostel', 'room', 'status']
    list_filter = ['hostel','room', 'status', 'mess']
    search_fields = ['student_name','student_id','student_branch']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'hostel', 'capacity', 'available']
    list_filter = ['hostel','capacity']

@admin.register(Parents)
class ParentsAdmin(admin.ModelAdmin):
    list_display = ['student', 'father_name', 'mother_name']
    search_fields = ['student__student_name', 'father_name', 'mother_name']

@admin.register(Visitors)
class VisitorsAdmin(admin.ModelAdmin):
    list_display = ['visitor_name', 'student', 'in_time', 'out_time']
    list_filter = ['in_time', 'out_time']
    search_fields = ['student__student_name','visitor_name']

@admin.register(Mess)
class MessAdmin(admin.ModelAdmin):
    list_display = ['mess_name','mess_fees']

@admin.register(Fees)
class FeesAdmin(admin.ModelAdmin):
    list_display = ['student', 'fees_status', 'student__id']
    list_filter = ['fees_status']
    search_fields = ['student__student_name', "student_id"]

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['staff_name', 'staff_duty', 'hostel']
    search_fields = ['staff_name']
    list_filter = ['hostel']
