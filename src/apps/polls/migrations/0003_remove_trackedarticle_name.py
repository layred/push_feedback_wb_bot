# Generated by Django 4.1.7 on 2023-03-07 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_rename_vendorcode_trackedarticle_article_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trackedarticle',
            name='name',
        ),
    ]