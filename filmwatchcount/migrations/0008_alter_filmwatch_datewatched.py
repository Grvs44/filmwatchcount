# Generated by Django 3.2.13 on 2022-07-10 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmwatchcount', '0007_auto_20220710_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwatch',
            name='DateWatched',
            field=models.DateField(blank=True, null=True, verbose_name='Date watched'),
        ),
    ]
