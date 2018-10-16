# Generated by Django 2.1.1 on 2018-10-05 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('introduce', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('upload', models.DateTimeField(auto_now_add=True)),
                ('like', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=True, to='user.user')),
            ],
        ),
    ]
