# Generated by Django 3.2 on 2023-01-16 07:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0009_auto_20230112_1956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='prefer',
            name='preference',
        ),
        migrations.AlterField(
            model_name='prefer',
            name='posting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prefers', to='community.posting'),
        ),
        migrations.AlterField(
            model_name='prefer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prefers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Bookmark',
        ),
        migrations.AddField(
            model_name='like',
            name='prefer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='community.prefer'),
        ),
        migrations.AddField(
            model_name='hate',
            name='prefer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hates', to='community.prefer'),
        ),
    ]
