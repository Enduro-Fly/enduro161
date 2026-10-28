from django.db import models
from django.contrib.auth.models import User

payment_choices = (('наличными', 'Наличными'), ('картой', 'Банковской картой'), ('СБП', 'СБП'))
status_choices = (('в обработке', 'В обработке'), ('подтверждена', 'Подтверждена'), ('исполнена', 'Завершена'), ('отменена', 'Отменена'))
type_choices = (
    ('KTM EXC 250', 'KTM EXC 250 — 3 500 ₽/час'),
    ('KTM EXC 300', 'KTM EXC 300 — 4 000 ₽/час'),
    ('Husqvarna TE 250', 'Husqvarna TE 250 — 3 800 ₽/час'),
    ('Kayo T4 250', 'Kayo T4 250 — 2 000 ₽/час'),
)

class zayavka(models.Model):
    type = models.CharField(max_length=30, verbose_name='мотоцикл', choices=type_choices)
    datetime = models.DateTimeField(verbose_name='дата и время начала')
    hours = models.PositiveSmallIntegerField(default=2, verbose_name='длительность, часов')
    price = models.PositiveIntegerField(default=7000, verbose_name='стоимость, ₽')
    payment = models.CharField(max_length=30, verbose_name='способ оплаты', choices=payment_choices)
    status = models.CharField(max_length=30, verbose_name='статус бронирования', choices=status_choices, default='в обработке')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', null=True)

    def __str__(self):
        return f'{self.type} | {self.datetime:%d.%m.%Y %H:%M} | {self.status}'

    class Meta:
        verbose_name = 'бронирование'
        verbose_name_plural = 'бронирования'
        ordering = ['-datetime']

class Review(models.Model):
    text = models.TextField(verbose_name='отзыв')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    zayavka = models.OneToOneField(zayavka, on_delete=models.CASCADE, verbose_name='бронирование')
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')

    def __str__(self):
        return f'{self.user.username} | {self.createdAt:%d.%m.%Y}'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
