# Generated by Django 4.2.7 on 2023-11-11 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('v1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testmp3',
            name='file',
            field=models.FileField(null=True, upload_to='audio/'),
        ),
        migrations.AlterField(
            model_name='testmp3',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
