# Generated by Django 3.2 on 2023-02-07 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reality', '0013_reality_secondname'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkerRTMS',
            fields=[
                ('RTMSkaptName', models.CharField(max_length=51, primary_key=True, serialize=False)),
                ('kaptCode', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'LinkerRTMS',
            },
        ),
        migrations.CreateModel(
            name='RTMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=41, null=True)),
                ('year', models.CharField(max_length=4, null=True)),
                ('month', models.CharField(max_length=2, null=True)),
                ('day', models.CharField(max_length=6, null=True)),
                ('useArea', models.FloatField(default=0.0)),
                ('jibun', models.CharField(max_length=11, null=True)),
                ('floor', models.CharField(max_length=4, null=True)),
                ('cancelType', models.CharField(max_length=1, null=True)),
                ('cancelDay', models.CharField(max_length=8, null=True)),
                ('reqGBN', models.CharField(max_length=10, null=True)),
                ('reality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RTMSs', to='reality.reality')),
            ],
            options={
                'db_table': 'RTMS',
            },
        ),
    ]
