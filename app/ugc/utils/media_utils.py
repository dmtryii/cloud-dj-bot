import os

from django.conf import settings
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube

from ..service.media_service import create_or_get_media


def download_video(url, chat):
    try:
        video = YouTube(url)
        stream = video.streams.filter(file_extension="mp4").first()
        video_path = os.path.join(settings.MEDIA_FILES, f'{video.title}.mp4')
        stream.download(output_path=settings.MEDIA_FILES, filename=f'{video.title}.mp4')
        create_or_get_media(url, chat)
        return video_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def convert_video_to_audio(path):
    try:
        video_clip = VideoFileClip(path)
        audio_clip = video_clip.audio
        audio_path = os.path.splitext(path)[0] + '.mp3'
        audio_clip.write_audiofile(audio_path, codec='mp3')
        video_clip.close()
        audio_clip.close()
        return audio_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
