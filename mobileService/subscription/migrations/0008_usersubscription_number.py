# Generated by Django 3.2.8 on 2021-11-01 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0007_alter_usersubscription_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='number',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='subscription.number'),
        ),
    ]
