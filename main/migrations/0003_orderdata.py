# Generated by Django 4.0.2 on 2022-03-17 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_customer_order_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('phone', models.TextField()),
            ],
        ),
    ]