# Generated by Django 3.2.7 on 2021-09-28 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_ticket_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='ticket_owner', to='app.user'),
            preserve_default=False,
        ),
    ]
