# Generated by Django 3.2.6 on 2021-08-14 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_address_eighteen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='eighteen',
            field=models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], default='Yes', max_length=4),
        ),
    ]
