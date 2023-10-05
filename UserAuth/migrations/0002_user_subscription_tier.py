# Generated by Django 4.2.1 on 2023-09-13 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscription_tier',
            field=models.CharField(choices=[('FREE', 'Free'), ('PREMIUM', 'Premium'), ('ENHANCED', 'Enhanced'), ('ULTIMATE', 'Ultimate')], default='FREE'),
        ),
    ]