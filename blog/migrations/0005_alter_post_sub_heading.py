# Generated by Django 3.2.5 on 2021-07-27 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_contact_postcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='sub_heading',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]
