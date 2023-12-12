# Generated by Django 4.2.8 on 2023-12-11 17:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0005_alter_habit_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='every_run',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10080)], verbose_name='запуск будет каждый указанный промежуток'),
        ),
        migrations.AlterField(
            model_name='habit',
            name='period',
            field=models.CharField(choices=[('minutes', 'minutes'), ('hours', 'hours'), ('days', 'days')], default='days', verbose_name='периодичность'),
        ),
    ]