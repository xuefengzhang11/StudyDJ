# Generated by Django 2.1.1 on 2018-10-08 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0018_auto_20181008_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='cs_category',
            field=models.ForeignKey(on_delete=True, to='course.category'),
        ),
        migrations.AlterField(
            model_name='course',
            name='introduce',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
