from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import (
    Student,
    Hostel,
    Parents,
    Room,
    Fees,
)
from authent.models import MyUser


def student_dashboard(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    student_exists = Student.objects.filter(student_id=user.student_id)
    if not student_exists:
        return redirect('dashboard')
    student = student_exists.first()
    context = {
        'student': student,
        'parent': Parents.objects.filter(student=student).first(),
        'fees': Fees.objects.filter(student=student).first()
    }
    return render(request, template_name='hostel/bookingdetails.html', context=context)


def dashboard(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if user.is_admin:
        return redirect('admin:index')
    student_exists = Student.objects.filter(student_id=user.student_id)
    if student_exists:
        return redirect('student_dashboard')
    ht = 'BOYS' if user.gender == 'Male' else 'GIRLS'
    hostel_list = Hostel.objects.filter(hostel_type=ht)
    data = {
        'hostel_list': hostel_list
    }
    return render(request, template_name='hostel/dashboard.html', context=data)


def signin_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        try:
            if user is not None:
                login(request, user)
                # if user.is_admin:
                #     return redirect('admin:index')
                return redirect('dashboard')
        except Exception as e:
            print(e)
            messages.error(request, ("e"))
            return redirect('login')
    
    return render(request, template_name='hostel/signin.html')


def register_user(request):
    if request.method == "POST":
        try:
            email = request.POST['email']
            student_id = request.POST['studentID']
            gender = request.POST['gender']
            password = request.POST['password']
            confirm_password = request.POST['confirmPassword']
            print(email)
            print(student_id)
            print(gender)
            print(password)
            print(confirm_password)
            # student = Student.objects.filter(student_id=student_id)
            # if Student.objects.filter(student_id=student_id):
            #     messages.error(request, ("Student with this ID already exists!"))
            #     return redirect('login')
            if not password == confirm_password:
                messages.error(request, ("Password and confirm password didn't match!"))
                return redirect('register')
            print("runnnnnnn")
            u = MyUser.objects.create_user(email=email, password=password)
            u.gender = str(gender)
            u.student_id = str(student_id)
            u.save()
            messages.success(request, ("Account Created Successfully!"))
            return redirect('login')
        except:
            messages.error(request, ("Something went wrong!"))
            return redirect('register')
        
    return render(request, template_name='hostel/register.html')


def booking(request, hostel_name):
    hostel = Hostel.objects.get(hostel_name=hostel_name)
    print(hostel)
    context = {
        'hostel':hostel,
    }
    if request.method == "POST":
        room_seater = int(request.POST["room_seater"])
        room = Room.objects.filter(hostel=hostel, capacity=room_seater).first()
        student_id = int(request.POST["student_id"])
        student_name = request.POST["student_name"]
        student_branch = request.POST["student_branch"]
        student_phone = request.POST["student_phone"]
        student_age = request.POST["student_age"]
        address_area = request.POST["address_area"]
        address_city = request.POST["address_city"]
        address_state = request.POST["address_state"]
        medical_status = request.POST["medical_status"]
        father_name = request.POST["father_name"]
        mother_name = request.POST["mother_name"]
        father_phone = request.POST["father_phone"]
        mother_phone = request.POST["mother_phone"]

        if not room:
            messages.error(request, ("Enter from available room seaters"))
            return render(request, template_name='hostel/booking.html', context=context) 
        if room.available <= 0:
            messages.error(request, ("Enter from available room seaters"))
            return render(request, template_name='hostel/booking.html', context=context)
        
        student = Student()
        student.hostel = hostel
        student.room = room
        student.student_id = student_id 
        student.student_name = student_name 
        student.student_branch = student_branch 
        student.student_phone = student_phone 
        student.student_age = student_age 
        student.address_area = address_area 
        student.address_city = address_city 
        student.address_state = address_state 
        student.medical_status = medical_status
        student.save()
        parent = Parents()
        parent.student = student
        parent.father_name = father_name
        parent.mother_name = mother_name
        parent.father_phone = father_phone
        parent.mother_phone = mother_phone
        parent.save()
        fee = Fees()
        fee.student = student
        fee.save()
        return redirect('student_dashboard')

    return render(request, template_name='hostel/booking.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('dashboard')