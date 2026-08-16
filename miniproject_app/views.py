from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Reservation,Room,SpecialRate,RoomCategory
from .forms import RegisterForm,BookingForm
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from datetime import datetime, date
# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully.")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user  = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('booking')
        else:
            messages.error(request,"invalid username or password")
    return render(request,'login.html')

@login_required
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)

            if instance.start_date < date.today() or instance.end_date < date.today():
                messages.error(request, "You cannot select past dates.")
                return redirect('booking')

            if instance.end_date <= instance.start_date:
                messages.error(request, "Check-out date must be after check-in date.")
                return redirect('booking')

            overlapping = Reservation.objects.filter(
                room=instance.room,
                start_date__lt=instance.end_date,
                end_date__gt=instance.start_date
                ).exclude(id=instance.id)
            if overlapping.exists():
                messages.error(request, "This room is already booked.")
            else:
                base_price = instance.room.category.base_price
                total_price = Decimal(0.00)
                number_days = (instance.end_date - instance.start_date).days
                for i in range(number_days):
                    current_date = instance.start_date + i * (instance.end_date - instance.start_date)/ number_days
                    special = SpecialRate.objects.filter(
                        room_category = instance.room.category,
                        start_date__lte = current_date,
                        end_date__gte = current_date,
                    ).first()
                    if special:
                        day_price = base_price * Decimal(special.rate_multiplier)
                    else:
                        day_price = base_price
                    total_price += day_price
                instance.total_price =round(total_price,2)
                instance.save()
                return render(request,'price.html',{'messages' : 'Booking successful!', 'total_price' : instance.total_price,'reservation': instance})

    else:
        form = BookingForm()
    return render(request, 'bookingform.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def check_available_rooms(request):
    categories = RoomCategory.objects.all()
    available_rooms = None

    if request.method == "POST":
        category_id = request.POST.get('category')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        if start_date < date.today() or end_date < date.today():
            error_message = "You cannot select past dates."
            return render(request, 'available_rooms.html', {
                'error_message': error_message,
                'categories': categories,
                'available_rooms': available_rooms
            })

        if end_date <= start_date:
            error_message = "End date must be after start date."
            return render(request, 'available_rooms.html', {
                'error_message': error_message,
                'categories': categories,
                'available_rooms': available_rooms
            })

        rooms = Room.objects.filter(category_id=category_id)
        available_rooms = []

        for room in rooms:
            reservations = Reservation.objects.filter(room=room)
            conflict = False
            for reservation in reservations:
                if reservation.start_date < end_date and reservation.end_date > start_date:
                    conflict = True
                    break
            if not conflict:
                available_rooms.append(room)

    return render(request, 'available_rooms.html', {
        'categories': categories,
        'available_rooms': available_rooms
    })

def confirm(request):
    return render(request, 'confirm.html')