# Generated by Django 4.1 on 2022-09-21 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filmwatchcount', '0008_alter_filmwatch_datewatched'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filmwatch',
            options={'ordering': ['id'], 'verbose_name_plural': 'Film watches'},
        ),
    ]
