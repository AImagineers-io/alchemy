# Generated by Django 5.1.2 on 2024-10-21 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='unstructured_data',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='processeddata',
            name='structured_data',
            field=models.JSONField(null=True),
        ),
    ]