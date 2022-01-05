# Generated by Django 3.2.10 on 2022-01-03 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_teacher_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='secret_key',
            name='group',
        ),
        migrations.AddField(
            model_name='secret_key',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='core.status', verbose_name='Кляч для ....'),
        ),
    ]
