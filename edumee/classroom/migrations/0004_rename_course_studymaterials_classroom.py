# Generated by Django 4.0.5 on 2022-08-05 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0003_studymaterials'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studymaterials',
            old_name='course',
            new_name='classroom',
        ),
    ]
