# Generated by Django 2.2 on 2021-04-02 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dragonchosen', '0004_auto_20210327_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=17)),
                ('ac', models.IntegerField()),
                ('hp', models.IntegerField()),
                ('race', models.CharField(max_length=17)),
                ('level', models.IntegerField()),
                ('charClass', models.CharField(max_length=17)),
                ('passivePerception', models.IntegerField()),
                ('speed', models.IntegerField()),
                ('alignment', models.CharField(max_length=17)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='heroes', to='dragonchosen.User')),
            ],
        ),
        migrations.DeleteModel(
            name='Character',
        ),
    ]
