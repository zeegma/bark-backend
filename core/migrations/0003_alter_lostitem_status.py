# Generated by Django 5.0.6 on 2025-04-12 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_claimform_ownership_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lostitem',
            name='status',
            field=models.CharField(choices=[('UC', 'Unclaimed'), ('CL', 'Claimed'), ('EX', 'Expired')], default='UC', max_length=2),
        ),
    ]
