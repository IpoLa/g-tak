# Generated by Django 4.0.4 on 2022-04-16 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gtakapp', '0002_alter_customer_avatar_alter_driver_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='location',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
