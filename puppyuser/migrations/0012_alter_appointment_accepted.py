# Generated by Django 3.2.8 on 2021-10-24 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puppyuser', '0011_auto_20211025_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='accepted',
            field=models.IntegerField(default=0),
        ),
    ]