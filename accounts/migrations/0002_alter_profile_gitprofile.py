# Generated by Django 4.0.6 on 2022-08-15 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gitprofile',
            field=models.URLField(blank=True, max_length=50, null=True, verbose_name='Профиль на GitHub'),
        ),
    ]