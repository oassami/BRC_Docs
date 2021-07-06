# Generated by Django 3.1.7 on 2021-07-05 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brc_app', '0003_employee_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('street', models.CharField(max_length=55)),
                ('city', models.CharField(max_length=55)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=10)),
                ('active', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('street', models.CharField(max_length=55)),
                ('city', models.CharField(max_length=55)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=10)),
                ('active', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trucking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('street', models.CharField(max_length=55)),
                ('city', models.CharField(max_length=55)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=10)),
                ('active', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
