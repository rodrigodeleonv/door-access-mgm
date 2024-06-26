# Generated by Django 5.0.4 on 2024-04-10 04:32

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RFIDTag',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('tag_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('owner', models.CharField(max_length=150, verbose_name='owner')),
                ('description', models.TextField(blank=True, default='')),
                ('valid_range_start', models.TimeField(default='00:00')),
                ('valid_range_end', models.TimeField(default='23:59:59')),
                ('active', models.BooleanField(default=True, help_text='The Tag (card) is active')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tags', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LogTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('allowed', models.BooleanField()),
                ('rfid_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rfid_tags', to='access_control.rfidtag')),
            ],
        ),
    ]
