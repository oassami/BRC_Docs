# Generated by Django 3.1.7 on 2021-06-24 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0002_auto_20210624_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='level',
            field=models.CharField(max_length=10),
        ),
    ]
