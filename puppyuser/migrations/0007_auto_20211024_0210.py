# Generated by Django 3.2.8 on 2021-10-24 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('puppyuser', '0006_alter_puppy_vaccinated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pupuser',
            name='puppy',
        ),
        migrations.AddField(
            model_name='puppy',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='puppyuser.pupuser'),
        ),
    ]
