# Generated by Django 4.0.5 on 2022-08-05 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0002_alter_classroom_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyMaterials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file_resource', models.FileField(null=True, upload_to='files/')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_material', to='classroom.classroom')),
            ],
        ),
    ]
