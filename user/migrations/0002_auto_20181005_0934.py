# Generated by Django 2.1.1 on 2018-10-05 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='icon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iconurl', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='userdetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('telephone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('birthday', models.DateField()),
                ('city', models.CharField(max_length=100)),
                ('introduce', models.CharField(max_length=200)),
                ('gender', models.ForeignKey(on_delete='True', to='user.gender')),
                ('icon', models.ForeignKey(on_delete=True, to='user.icon')),
                ('job', models.ForeignKey(on_delete=True, to='user.job')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
