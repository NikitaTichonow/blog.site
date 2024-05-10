# Generated by Django 5.0.3 on 2024-05-10 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotUserModel',
            fields=[
                ('chat_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия')),
                ('user_name', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Зарегистрирован')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Последняя активность')),
            ],
            options={
                'verbose_name': 'Пользователь бота',
                'verbose_name_plural': 'Пользователи бота',
                'ordering': ['-updated'],
            },
        ),
    ]
