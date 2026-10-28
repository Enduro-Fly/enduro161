from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('testapp', '0003_review')]
    operations = [
        migrations.AlterField(model_name='zayavka', name='type', field=models.CharField(choices=[('KTM EXC 250','KTM EXC 250 — 3 500 ₽/час'),('KTM EXC 300','KTM EXC 300 — 4 000 ₽/час'),('Husqvarna TE 250','Husqvarna TE 250 — 3 800 ₽/час'),('Kayo T4 250','Kayo T4 250 — 2 000 ₽/час')], max_length=30, verbose_name='мотоцикл')),
        migrations.AddField(model_name='zayavka', name='hours', field=models.PositiveSmallIntegerField(default=2, verbose_name='длительность, часов')),
        migrations.AddField(model_name='zayavka', name='price', field=models.PositiveIntegerField(default=7000, verbose_name='стоимость, ₽')),
        migrations.AlterField(model_name='zayavka', name='status', field=models.CharField(choices=[('в обработке','В обработке'),('подтверждена','Подтверждена'),('исполнена','Завершена'),('отменена','Отменена')], default='в обработке', max_length=30, verbose_name='статус бронирования')),
        migrations.AlterModelOptions(name='zayavka', options={'ordering':['-datetime'], 'verbose_name':'бронирование', 'verbose_name_plural':'бронирования'}),
    ]
