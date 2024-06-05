# Generated by Django 5.0.6 on 2024-06-04 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messenger_app', '0003_alter_message_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('date_published',), 'permissions': [('can_edit_message', 'user can edit message'), ('can_delete_message', 'user can delete message')]},
        ),
    ]