# Generated by Django 4.1.3 on 2024-12-19 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fapp', '0005_group_groupmember_groupexpense_groupbalance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupbalance',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
