# Generated by Django 3.2.6 on 2021-08-25 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_address_eighteen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='eighteen',
            field=models.CharField(choices=[('No', 'No'), ('Yes', 'Yes')], default='Yes', max_length=4),
        ),
    ]
