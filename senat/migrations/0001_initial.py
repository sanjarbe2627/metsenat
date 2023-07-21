# Generated by Django 4.2.3 on 2023-07-22 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_type', models.CharField(choices=[('physical', 'Physical person'), ('juridical', 'Legal entity')], default='physical', max_length=15)),
                ('fullname', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('money', models.BigIntegerField(default=0)),
                ('company_name', models.CharField(blank=True, max_length=150, null=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('moderation', 'IN Moderation'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')], default='moderation', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Sponsor',
                'verbose_name_plural': 'Sponsors',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Universities',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('student_type', models.CharField(choices=[('bachelor', 'Bachelor'), ('master', 'Master')], default='bachelor', max_length=15)),
                ('contract', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('university', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student', to='senat.university')),
            ],
            options={
                'verbose_name_plural': 'Students',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsorship', to='senat.sponsor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsorship', to='senat.student')),
            ],
            options={
                'verbose_name_plural': 'Sponsorships',
                'ordering': ['-created_at'],
            },
        ),
    ]
