# Generated by Django 5.1.2 on 2024-12-03 00:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_document_unstructured_data_logentry'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('SUCCESS', 'Success'), ('FAILURE', 'Failure')], default='PENDING', max_length=50)),
                ('progress', models.IntegerField(default=0)),
                ('result', models.TextField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='LogEntry',
        ),
    ]