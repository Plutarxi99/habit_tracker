# Generated by Django 4.2.8 on 2023-12-11 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_chat_id_tg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='chat_id_tg',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='для отправки ботом уведомлений'),
        ),
    ]
