# Generated by Django 5.1.2 on 2024-11-03 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_document_unstructured_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='publication_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='source_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]