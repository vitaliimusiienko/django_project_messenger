# Generated by Django 5.0.6 on 2024-06-10 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger_app', '0009_messages_receiver_alter_messages_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_log', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('message', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='log', to='messenger_app.messages')),
            ],
        ),
    ]
