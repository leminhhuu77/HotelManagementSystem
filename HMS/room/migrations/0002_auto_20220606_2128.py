# Generated by Django 3.0.8 on 2022-06-06 14:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220606_2128'),
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('totalAmount', models.FloatField()),
                ('summary', models.TextField(null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Guest')),
            ],
        ),
        migrations.RemoveField(
            model_name='refund',
            name='guest',
        ),
        migrations.RemoveField(
            model_name='refund',
            name='reservation',
        ),
        migrations.RemoveField(
            model_name='roomservices',
            name='curBooking',
        ),
        migrations.RemoveField(
            model_name='roomservices',
            name='room',
        ),
        migrations.AlterField(
            model_name='room',
            name='roomType',
            field=models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=20),
        ),
        migrations.DeleteModel(
            name='Dependees',
        ),
        migrations.DeleteModel(
            name='Refund',
        ),
        migrations.DeleteModel(
            name='RoomServices',
        ),
        migrations.AddField(
            model_name='bills',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.Room'),
        ),
    ]
