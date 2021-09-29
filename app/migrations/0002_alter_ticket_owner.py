# Generated by Django 3.2.7 on 2021-09-28 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='owner',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, related_name='ticket_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
