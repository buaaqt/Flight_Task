# Generated by Django 2.1.7 on 2019-04-13 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=64)),
                ('date', models.CharField(max_length=64)),
            ],
        ),
    ]
