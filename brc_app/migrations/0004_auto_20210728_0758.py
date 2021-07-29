# Generated by Django 3.1.7 on 2021-07-28 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brc_app', '0003_auto_20210718_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prodproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produced', to='brc_app.product'),
        ),
        migrations.AlterField(
            model_name='receive',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received', to='brc_app.product'),
        ),
    ]
