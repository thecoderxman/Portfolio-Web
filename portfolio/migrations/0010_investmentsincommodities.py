# Generated by Django 3.0.3 on 2020-05-01 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0009_investmentsinindices'),
    ]

    operations = [
        migrations.CreateModel(
            name='investmentsincommodities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('price', models.FloatField(blank=True, default=None, null=True)),
                ('date_created', models.CharField(max_length=200, null=True)),
                ('current_time', models.CharField(max_length=200, null=True)),
                ('gain_loss', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
