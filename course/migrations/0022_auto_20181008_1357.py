# Generated by Django 2.1.1 on 2018-10-08 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0021_auto_20181008_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='cs_category',
            field=models.ForeignKey(on_delete=True, to='course.category'),
        ),
    ]
