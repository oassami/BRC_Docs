# Generated by Django 3.1.7 on 2021-07-18 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brc_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='receive',
            old_name='received_by',
            new_name='by_employee',
        ),
        migrations.RenameField(
            model_name='ship',
            old_name='shipped_by',
            new_name='by_employee',
        ),
    ]
