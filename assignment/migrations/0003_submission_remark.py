# Generated by Django 3.0.3 on 2020-07-12 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0002_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='remark',
            field=models.CharField(max_length=255, null=True),
        ),
    ]