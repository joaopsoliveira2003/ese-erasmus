# Generated by Django 3.2.2 on 2021-05-11 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20210511_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.category'),
        ),
    ]