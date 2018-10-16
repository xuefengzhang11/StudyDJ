# Generated by Django 2.1.1 on 2018-10-01 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20180929_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='learn',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='course',
            name='cs_category',
            field=models.ForeignKey(on_delete=True, to='course.category'),
        ),
    ]
