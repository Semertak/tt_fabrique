# Generated by Django 2.2.10 on 2021-08-22 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll_app', '0004_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='login',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='token',
            field=models.TextField(blank=True),
        ),
    ]
