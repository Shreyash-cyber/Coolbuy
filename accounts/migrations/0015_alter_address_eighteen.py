# Generated by Django 3.2.6 on 2021-08-25 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_address_eighteen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='eighteen',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes', max_length=4),
        ),
    ]
