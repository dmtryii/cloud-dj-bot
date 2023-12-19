# Generated by Django 5.0 on 2023-12-19 11:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Create At')),
            ],
            options={
                'verbose_name': 'Hashtag',
                'verbose_name_plural': 'Hashtags',
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=255, unique=True, verbose_name='Media ID')),
                ('telegram_video_file_id', models.CharField(verbose_name='Telegram Video File ID')),
                ('telegram_audio_file_id', models.CharField(verbose_name='Telegram Audio File ID')),
                ('title', models.TextField(verbose_name='Title')),
                ('url', models.TextField(verbose_name='Url')),
                ('channel', models.TextField(verbose_name='Channel')),
                ('duration', models.IntegerField(verbose_name='Duration')),
                ('date_of_addition', models.DateTimeField(auto_now_add=True, verbose_name='Date of addition')),
            ],
            options={
                'verbose_name': 'Media',
                'verbose_name_plural': 'Medias',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.BigIntegerField(unique=True, verbose_name='Profile ID')),
                ('username', models.TextField(null=True, verbose_name='Username')),
                ('first_name', models.TextField(null=True, verbose_name='First Name')),
                ('last_name', models.TextField(null=True, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('first_login_date', models.DateTimeField(auto_now_add=True, verbose_name='First login date')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Active')),
                ('state', models.CharField(choices=[('BASIC', 'Basic State'), ('WAIT_FOR_MEDIA', 'Wait for Media'), ('WAIT_FOR_EMAIL', 'Wait for Email')], default='BASIC')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='MediaProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Date Added')),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.media', verbose_name='Media')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Media Profile',
                'verbose_name_plural': 'Media Profiles',
                'unique_together': {('media', 'profile')},
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.PositiveIntegerField(verbose_name='Message ID')),
                ('content_type', models.TextField(verbose_name='Content Type')),
                ('text', models.TextField(verbose_name='Text')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Time of receiving')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.profile', verbose_name='Profile')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
        migrations.CreateModel(
            name='MediaProfileHashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.hashtag', verbose_name='Hashtag')),
                ('media_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ugc.mediaprofile', verbose_name='MediaProfile')),
            ],
            options={
                'verbose_name': 'Media Profile Hashtag',
                'verbose_name_plural': 'Media Profiles Hashtags',
                'unique_together': {('media_profile', 'hashtag')},
            },
        ),
    ]
