# Generated by Django 3.2 on 2023-02-07 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reality', '0016_alter_linkerrtms_kaptcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='rtms',
            name='serialNumber',
            field=models.CharField(max_length=41, null=True, unique=True),
        ),
    ]
