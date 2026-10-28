from django.contrib import admin
from .models import zayavka, Review

@admin.register(zayavka)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'datetime', 'hours', 'price', 'status', 'user')
    list_filter = ('status', 'type', 'payment')
    search_fields = ('user__username', 'type')

admin.site.register(Review)
admin.site.site_header = 'ENDURO 161 / Администрирование'
