# Generated by Django 3.0.8 on 2022-06-14 15:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_auto_20220606_2128'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Employee',
            new_name='Manager',
        ),
    ]
