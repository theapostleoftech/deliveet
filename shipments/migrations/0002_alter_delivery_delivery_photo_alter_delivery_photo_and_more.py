# Generated by Django 4.2.13 on 2024-07-09 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='delivery_photo',
            field=models.ImageField(blank=True, null=True, upload_to='./media/delivery/delivery/'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='./media/delivery/'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='pickup_photo',
            field=models.ImageField(blank=True, null=True, upload_to='./media/delivery/pickup/'),
        ),
    ]
