from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import zayavka, Review, type_choices
from .forms import CreateUserForm, CreateZayavkaForm

BIKES = [
    {
        'name': 'KTM EXC 250',
        'kind': 'ЭНДУРО · 2T',
        'price': 10500,
        'desc': 'Лёгкий и резкий, для техничных маршрутов.',
        'tag': 'ХИТ',
        'image': '/static/images/bikes/ktm-exc-250.jpg',
    },
    {
        'name': 'KTM EXC 300',
        'kind': 'ЭНДУРО · 2T',
        'price': 10000,
        'desc': 'Максимум тяги для сложных подъёмов.',
        'tag': 'PRO',
        'image': '/static/images/bikes/ktm-exc-300.jpg',
    },
    {
        'name': 'Husqvarna TE 250',
        'kind': 'ЭНДУРО · 2T',
        'price': 10800,
        'desc': 'Баланс мощности, контроля и комфорта.',
        'tag': 'NEW',
        'image': '/static/images/bikes/husqvarna-te-250.jpg',
    },
    {
        'name': 'Kayo T4 250',
        'kind': 'ЭНДУРО · 4T',
        'price': 3000,
        'desc': 'Отличный выбор для первого выезда.',
        'tag': 'START',
        'image': '/static/images/bikes/kayo-t4-250.jpg',
    },
]

def index(request):
    return render(request, 'index.html', {'bikes': BIKES, 'reviews': Review.objects.select_related('user').order_by('-createdAt')[:3]})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Аккаунт создан. Можно бронировать мотоцикл!')
        return redirect('home')
    return render(request, 'register.html', {'form': form})

@login_required
def create(request):
    form = CreateZayavkaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        rate = dict((name, price) for name, price in [('KTM EXC 250',3500),('KTM EXC 300',4000),('Husqvarna TE 250',3800),('Kayo T4 250',2000)])
        booking.price = rate[booking.type] * booking.hours
        start, end = booking.datetime, booking.datetime + timedelta(hours=booking.hours)
        conflicts = zayavka.objects.filter(type=booking.type, status__in=['в обработке','подтверждена']).filter(datetime__lt=end, datetime__gt=start-timedelta(hours=8))
        for old in conflicts:
            old_end = old.datetime + timedelta(hours=old.hours)
            if start < old_end and end > old.datetime:
                form.add_error('datetime', 'Этот мотоцикл уже забронирован на выбранное время. Выберите другой слот.')
                break
        if not form.errors:
            booking.save()
            messages.success(request, f'Заявка создана! Стоимость: {booking.price:,} ₽'.replace(',', ' '))
            return redirect('bookings')
    return render(request, 'create.html', {'form': form, 'bikes': BIKES})

@login_required
def bookings(request):
    if request.method == 'POST' and request.POST.get('action') == 'cancel':
        booking = get_object_or_404(zayavka, pk=request.POST.get('booking_id'), user=request.user)
        if booking.status == 'в обработке' and booking.datetime > timezone.now():
            booking.status = 'отменена'
            booking.save(update_fields=['status'])
            messages.success(request, 'Бронирование отменено.')
        else:
            messages.error(request, 'Это бронирование уже нельзя отменить онлайн.')
        return redirect('bookings')
    if request.method == 'POST' and request.POST.get('action') == 'review':
        booking = get_object_or_404(zayavka, pk=request.POST.get('booking_id'), user=request.user, status='исполнена')
        if not hasattr(booking, 'review') and request.POST.get('review','').strip():
            Review.objects.create(text=request.POST['review'].strip(), user=request.user, zayavka=booking)
            messages.success(request, 'Спасибо за отзыв!')
        return redirect('bookings')
    return render(request, 'bookings.html', {'bookings': zayavka.objects.filter(user=request.user).select_related('user'), 'now': timezone.now()})
