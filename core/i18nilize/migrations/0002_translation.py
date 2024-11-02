# Generated by Django 5.1.1 on 2024-10-18 02:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('i18nilize', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_word', models.CharField(max_length=255)),
                ('translated_word', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255)),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='i18nilize.token')),
            ],
        ),
    ]
