# Generated by Django 4.2.8 on 2023-12-10 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit', '0002_alter_habit_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='period',
            field=models.CharField(choices=[('hours', 'hours'), ('days', 'days'), ('week', 'one_to_week')], default='days', verbose_name='периодичность'),
        ),
    ]
