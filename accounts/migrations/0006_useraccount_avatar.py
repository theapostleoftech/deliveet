# Generated by Django 4.2.13 on 2024-07-09 08:11

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_useraccount_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='avatar',
            field=versatileimagefield.fields.VersatileImageField(blank=True, default='', null=True, upload_to='media/avatars/', verbose_name='Avatar'),
        ),
    ]
