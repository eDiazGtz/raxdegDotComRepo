# Generated by Django 2.2 on 2021-03-27 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dragonchosen', '0003_auto_20210327_1136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='strSave',
            new_name='dm',
        ),
    ]