# Generated by Django 3.2 on 2023-02-05 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reality', '0012_auto_20230204_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='reality',
            name='secondName',
            field=models.CharField(max_length=51, null=True),
        ),
    ]
