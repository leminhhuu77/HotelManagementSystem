from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.db.models import Q, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

from django.contrib import messages
from datetime import datetime, date, timedelta
import random

# Own imports
from accounts.models import *
from room.models import *
from .forms import *
# Create your views here.

def register_page(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                if (len(User.objects.filter(email=request.POST.get("email"))) != 0):
                    messages.error(
                        request, 'Email address is alredy taken')
                    return redirect('login')

                user = form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get(name="guest")
                user.groups.add(group)

                curGuest = Guest(
                    user=user, phoneNumber=request.POST.get("phoneNumber"))
                curGuest.save()

                messages.success(
                    request, 'Guest Account Was Created Succesfuly For ' + username)

                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username or Password is incorrect")

        context = {}
        return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def guests(request):
    role = str(request.user.groups.all()[0])
    path = role + "/"

    topRange = Booking.objects.all().values("guest").annotate(
        total=Count("guest")).order_by("-total")
    topLimit = 10
    topList = []
    for t in topRange:
        if len(topList) > 10:
            break
        else:
            topList.append(Guest.objects.get(id=t.get("guest")))

    bookings = Booking.objects.all()
    fd = datetime.combine(date.today()-timedelta(days=30), datetime.min.time())
    ld = datetime.combine(date.today(), datetime.min.time())
    guests = []

    for b in bookings:
        if b.endDate >= fd.date() and b.startDate <= ld.date():
            if b.guest not in guests:
                guests.append(b.guest)

    if request.method == "POST":
        if "filterDate" in request.POST:

            if request.POST.get("f_day") == "" and request.POST.get("l_day") == "":
                guests = Guest.objects.all()

                context = {
                    "role": role,
                    "guests": guests,
                    "fd": "",
                    "ld": ""
                }
                return render(request, path + "guests.html", context)

            if request.POST.get("f_day") == "":
                fd = datetime.strptime("1970-01-01", '%Y-%m-%d')
            else:
                fd = request.POST.get("f_day")
                fd = datetime.strptime(fd, '%Y-%m-%d')

            if request.POST.get("l_day") == "":
                ld = datetime.strptime("2030-01-01", '%Y-%m-%d')
            else:
                ld = request.POST.get("l_day")
                ld = datetime.strptime(ld, '%Y-%m-%d')

            for b in bookings:
                if b.endDate >= fd.date() and b.startDate <= ld.date():
                    if b.guest not in guests:
                        guests.append(b.guest)

        if "filterGuest" in request.POST:
            guests = Guest.objects.all()
            users = User.objects.all()
            if (request.POST.get("id") != ""):
                users = users.filter(
                    id__contains=request.POST.get("id"))
                guests = guests.filter(user__in=users)

            if (request.POST.get("name") != ""):
                users = users.filter(
                    Q(first_name__contains=request.POST.get("name")) | Q(last_name__contains=request.POST.get("name")))
                guests = guests.filter(user__in=users)

            if (request.POST.get("email") != ""):
                users = users.filter(email__contains=request.POST.get("email"))
                guests = guests.filter(user__in=users)

            if (request.POST.get("number") != ""):
                guests = guests.filter(
                    phoneNumber__contains=request.POST.get("number"))

            context = {
                "role": role,
                "guests": guests,
                "id": request.POST.get("id"),
                "name": request.POST.get("name"),
                "email": request.POST.get("email"),
                "number": request.POST.get("number")
            }
            return render(request, path + "guests.html", context)

        if "top" in request.POST:
            topRange = Booking.objects.all().values("guest").annotate(
                total=Count("guest")).order_by("-total")
            topList = []
            topLimit = request.POST.get("top")
            for t in topRange:
                if len(topList) >= int(topLimit):
                    break
                else:
                    topList.append(Guest.objects.get(id=t.get("guest")))
            context = {
                "role": role,
                "guests": guests,
                "topList": topList,
                "topLimit": topLimit,
                "fd": fd,
                "ld": ld
            }
            return render(request, path + "guests.html", context)
    context = {
        "role": role,
        "guests": guests,
        "topList": topList,
        "topLimit": topLimit,
        "fd": fd,
        "ld": ld
    }
    return render(request, path + "guests.html", context)

@ login_required(login_url='login')
def guest_edit(request, pk):
    role = str(request.user.groups.all()[0])
    path = role + "/"
    tempuser = User.objects.get(id=pk)
    guest = Guest.objects.get(user=tempuser)
    form1 = editGuest(instance=guest)
    form2 = editUser(instance=tempuser)

    context = {
        "role": role,
        "guest": guest,
        "form1": form1,
        "form2": form2,
        "user": tempuser,
    }

    if request.method == "POST":
        form1 = editGuest(request.POST, instance=guest)
        form2 = editUser(request.POST, instance=tempuser)
        if form1.is_valid and form2.is_valid:
            form1.save()
            form2.save()

    return render(request, path + "guest-edit.html", context)


@login_required(login_url='login')
def guest_profile(request, pk):
    tempUser = User.objects.get(id=pk)
    guest = Guest.objects.get(user=tempUser)

    if request.method == 'POST':
        tempUser.first_name = request.POST.get("first_name")
        tempUser.last_name = request.POST.get("last_name")
        guest.phoneNumber = request.POST.get("phoneNumber")
        tempUser.save()
        guest.save()
        return redirect("home")
    role = str(request.user.groups.all()[0])
    path = role + "/"

    bookings = Booking.objects.filter(guest=guest)
    context = {
        "role": role,
        "guest": guest,
        "bookings": bookings
    }
    return render(request, path + "guest-profile.html", context)

@login_required(login_url='login')
def employee_details(request, pk):
    if request.method == 'POST':
        user = User.objects.get(id=pk)
        employee = Employee.objects.get(user=user)
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        employee.phoneNumber = request.POST.get("phoneNumber")
        user.save()
        employee.save()
        return redirect("home")

    role = str(request.user.groups.all()[0])
    path = role + "/"

    tempUser = User.objects.get(id=pk)
    employee = Employee.objects.get(user=tempUser)
    context = {
        "role": role,
        "employee": employee,
    }
    return render(request, path + "employee-profile.html", context)