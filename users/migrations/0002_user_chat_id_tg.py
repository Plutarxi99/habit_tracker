# Generated by Django 5.0 on 2023-12-10 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chat_id_tg',
            field=models.CharField(default='534346799', max_length=30, verbose_name='для отправки ботом уведомлений'),
            preserve_default=False,
        ),
    ]
