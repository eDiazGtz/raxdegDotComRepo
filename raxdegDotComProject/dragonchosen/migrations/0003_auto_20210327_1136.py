# Generated by Django 2.2 on 2021-03-27 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dragonchosen', '0002_user_strsave'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email',
            new_name='username',
        ),
    ]
