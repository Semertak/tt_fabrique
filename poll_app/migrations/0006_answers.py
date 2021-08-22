# Generated by Django 2.2.10 on 2021-08-22 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll_app', '0005_auto_20210822_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll_app.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll_app.Users')),
            ],
        ),
    ]