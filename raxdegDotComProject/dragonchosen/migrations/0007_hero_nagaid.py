# Generated by Django 2.2 on 2021-04-02 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dragonchosen', '0006_auto_20210401_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='nagaId',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]