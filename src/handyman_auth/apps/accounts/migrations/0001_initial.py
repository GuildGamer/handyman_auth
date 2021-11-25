# Generated by Django 3.2.9 on 2021-11-25 22:12

from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('country_code', models.CharField(max_length=254)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='HandyManUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', phone_field.models.PhoneField(max_length=31)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('token', models.TextField(default='')),
                ('firstname', models.CharField(max_length=254)),
                ('lastname', models.CharField(max_length=254)),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1)),
                ('avatar', models.ImageField(upload_to='avatars/')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.country', verbose_name='country')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
