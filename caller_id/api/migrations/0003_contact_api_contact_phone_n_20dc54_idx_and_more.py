# Generated by Django 5.1.4 on 2025-01-07 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_customuser_email_alter_customuser_full_name_and_more'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='contact',
            index=models.Index(fields=['phone_number'], name='api_contact_phone_n_20dc54_idx'),
        ),
        migrations.AddIndex(
            model_name='contact',
            index=models.Index(fields=['full_name'], name='api_contact_full_na_438bdc_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['phone_number'], name='api_customu_phone_n_60713e_idx'),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['full_name'], name='api_customu_full_na_3cacee_idx'),
        ),
        migrations.AddIndex(
            model_name='spamreport',
            index=models.Index(fields=['phone_number'], name='api_spamrep_phone_n_054e20_idx'),
        ),
        migrations.AddConstraint(
            model_name='contact',
            constraint=models.UniqueConstraint(fields=('phone_number', 'owner'), name='unique_owner_contact'),
        ),
        migrations.AddConstraint(
            model_name='spamreport',
            constraint=models.UniqueConstraint(fields=('phone_number', 'reported_by'), name='unique_spam_report'),
        ),
    ]
