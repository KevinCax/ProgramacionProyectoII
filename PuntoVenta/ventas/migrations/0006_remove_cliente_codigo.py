# Generated by Django 5.1 on 2024-09-25 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_rename_nitocui_cliente_nit_cui_alter_cliente_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='codigo',
        ),
    ]