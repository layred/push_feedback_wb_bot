# Generated by Django 4.1.7 on 2023-03-08 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_feedbackphoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='personal',
            name='sheetId',
            field=models.IntegerField(blank=True, null=True, verbose_name='ID листа'),
        ),
    ]
