# Generated by Django 3.1.7 on 2021-07-08 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('address', models.CharField(max_length=55)),
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
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(max_length=10, unique=True)),
                ('first_name', models.CharField(max_length=55)),
                ('last_name', models.CharField(max_length=55)),
                ('level', models.CharField(max_length=10)),
                ('active', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Finished',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lot_num', models.CharField(max_length=55)),
                ('prod_name', models.CharField(max_length=55)),
                ('best_by', models.DateField()),
                ('qty', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Incoming',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lot_num', models.CharField(max_length=55)),
                ('prod_name', models.CharField(max_length=55)),
                ('best_by', models.DateField()),
                ('qty', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('address', models.CharField(max_length=55)),
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
            name='Truck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=55)),
                ('address', models.CharField(max_length=55)),
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
            name='Ship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ship_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='brc_app.supplier')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipped_by', to='brc_app.employee')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipped_product', to='brc_app.incoming')),
                ('trucker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipped_truckers', to='brc_app.truck')),
            ],
        ),
        migrations.CreateModel(
            name='Receive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receive_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recieved_by', to='brc_app.employee')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_product', to='brc_app.incoming')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to='brc_app.supplier')),
                ('trucker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_truckers', to='brc_app.truck')),
            ],
        ),
    ]
