# Generated by Django 4.1.6 on 2023-02-02 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("community", "0017_alter_user_nickname"),
    ]

    operations = [
        migrations.RemoveField(model_name="user", name="email",),
        migrations.RemoveField(model_name="user", name="name",),
    ]
