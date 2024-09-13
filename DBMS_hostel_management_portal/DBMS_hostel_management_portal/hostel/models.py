from django.db import models

# Create your models here.

class Hostel(models.Model):
    HOSTELTYPE = [
        ('BOYS', 'BOYS'),
        ('GIRLS', 'GIRLS')
    ]
    hostel_name = models.CharField(max_length=30,primary_key=True)
    hostel_type = models.CharField(choices=HOSTELTYPE, max_length=30, null=True)

    def __str__(self):
        return self.hostel_name
    
    @property
    def no_of_rooms(self):
        rooms = len(self.hostel_room.all())
        return rooms
    
    @property
    def no_of_students(self):
        students = len(self.hostel_students.all())
        return students
    
    @property
    def room_seaters(self):
        rooms_o = self.hostel_room.all()
        rooms = [i.capacity for i in rooms_o]
        rooms = list(dict.fromkeys(rooms))
        print(rooms)
        room_seaters = [{'capacity':i} for i in rooms if rooms_o[rooms.index(i)].available > 0]
        return room_seaters


class Room(models.Model):
    hostel = models.ForeignKey(Hostel,related_name="hostel_room", on_delete=models.CASCADE)
    room_name = models.CharField(max_length=10,primary_key=True)
    capacity = models.IntegerField()
    room_fees = models.IntegerField()

    def __str__(self):
        return self.room_name
    
    @property
    def available(self):
        students = len(self.room_students.all())
        available = self.capacity - students
        return available
        


class Mess(models.Model):
    mess_name = models.CharField(max_length = 13)
    mess_fees = models.IntegerField()

    def __str__(self):
        return self.mess_name


class Student(models.Model):
    STATUS = [
        ('REQUESTED', 'REQUESTED'),
        ('PENDING', 'PENDING'),
        ('ASSIGNED', 'ASSIGNED'),
    ]
    hostel = models.ForeignKey(Hostel,related_name="hostel_students", on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room,related_name="room_students", on_delete=models.CASCADE, null=True)
    mess = models.ForeignKey(Mess,related_name="mess_students", on_delete=models.CASCADE, null=True)
    student_id = models.IntegerField(primary_key=True)
    student_name = models.CharField(max_length = 30)
    student_branch = models.CharField(max_length = 30)
    student_phone = models.CharField(max_length=13)
    student_age = models.IntegerField()
    address_area = models.CharField(max_length = 100)
    address_city = models.CharField(max_length = 40)
    address_state = models.CharField(max_length = 40)
    medical_status = models.CharField(max_length = 300)
    status = models.CharField(max_length=50, choices=STATUS, default='REQUESTED')
    
    def __str__(self):
        return self.student_name
    
    # add check if student is boy then add in boys hostel only and viceversa
    
    # change status to assinged only after adding hostel


class Fees(models.Model):
    FEE_STATUS = [
        ('PAID', 'PAID'),
        ('NOT PAID', 'NOT PAID')
    ]
    student = models.ForeignKey(Student,related_name = "student_fees", on_delete=models.CASCADE)
    fees_status = models.CharField(max_length=10, choices=FEE_STATUS, default='NOT PAID')

    def __str__(self):
        return self.student.student_name

    @property
    def student__id(self):
        student_id = self.student.student_id
        return student_id
    

class Staff(models.Model):
    hostel = models.ForeignKey(Hostel,related_name="hostel_staff",on_delete=models.CASCADE)
    staff_id = models.IntegerField(primary_key=True)
    staff_name = models.CharField(max_length=30)
    staff_duty = models.CharField(max_length=30)

    def __str__(self):
        return self.staff_name


class Parents(models.Model):
    student = models.ForeignKey(Student, related_name="student_parents", on_delete=models.CASCADE)
    father_name = models.CharField(max_length = 30)
    mother_name = models.CharField(max_length = 30)
    father_phone = models.CharField(max_length=13)
    mother_phone = models.CharField(max_length=13)

    def __str__(self):
        return self.student.student_name


class Visitors(models.Model):
    student = models.ForeignKey(Student,related_name="student_visitors",on_delete=models.CASCADE)
    out_time = models.DateTimeField()
    in_time = models.DateTimeField()
    visitor_phone = models.CharField(max_length=13)
    visitor_name = models.CharField(max_length = 30)

    def __str__(self):
        return self.visitor_name
