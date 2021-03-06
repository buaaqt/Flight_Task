# Generated by Django 2.1.7 on 2019-04-13 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airplane',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('number', models.TextField()),
                ('departure', models.TextField()),
                ('arrival', models.TextField()),
                ('depart_time', models.TextField()),
                ('arrive_time', models.TextField()),
                ('spendtime', models.TextField()),
                ('airline', models.TextField()),
                ('price', models.TextField()),
                ('embargo', models.TextField()),
                ('delay_rate', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accout', models.TextField()),
                ('password', models.TextField()),
                ('plane_marked', models.TextField()),
                ('if_picked', models.TextField()),
                ('information', models.TextField()),
                ('if_manage', models.TextField()),
            ],
        ),
    ]
