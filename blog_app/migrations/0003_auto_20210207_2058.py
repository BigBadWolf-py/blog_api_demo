# Generated by Django 3.1.6 on 2021-02-07 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_auto_20210207_1949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcomment',
            old_name='blog',
            new_name='post',
        ),
    ]
