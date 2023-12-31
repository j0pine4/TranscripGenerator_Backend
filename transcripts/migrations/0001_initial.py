# Generated by Django 4.2.1 on 2023-09-30 09:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoID', models.CharField(max_length=150)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('type', models.CharField(choices=[('TRANSCRIPT', 'Transcript'), ('GENERATED', 'AI Generated')], default='TRANSCRIPT', max_length=150)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
