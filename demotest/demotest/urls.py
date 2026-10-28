from django.contrib import admin
from django.urls import path, include
from testapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('create/', views.create, name='create'),
    path('bookings/', views.bookings, name='bookings'),
]
