# Generated by Django 2.2.3 on 2019-07-22 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='question',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
