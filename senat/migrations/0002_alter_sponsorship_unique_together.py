# Generated by Django 4.2.3 on 2023-07-23 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('senat', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sponsorship',
            unique_together={('sponsor', 'student')},
        ),
    ]