# Generated by Django 2.0 on 2022-12-14 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20221202_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='discord_account',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
