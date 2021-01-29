# Generated by Django 3.1.5 on 2021-01-29 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('destination', models.CharField(max_length=50, null=True)),
                ('origin', models.CharField(max_length=50, null=True)),
                ('amount', models.FloatField(null=True)),
            ],
        ),
    ]
