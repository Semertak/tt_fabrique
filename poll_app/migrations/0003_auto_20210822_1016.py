# Generated by Django 2.2.10 on 2021-08-22 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poll_app', '0002_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='poll_id',
            new_name='poll',
        ),
    ]