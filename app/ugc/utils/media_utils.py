import os

from django.conf import settings
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube


def download_video(url: str) -> str | None:
    try:
        video = YouTube(url)
        stream = video.streams.filter(file_extension="mp4").first()
        video_path = os.path.join(settings.MEDIA_FILES, f'{video.title}.mp4')
        stream.download(output_path=settings.MEDIA_FILES, filename=f'{video.title}.mp4')
        return video_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def convert_video_to_audio(url: str) -> str | None:
    try:
        video_path = download_video(url)
        if video_path is None:
            return None

        audio_path = os.path.splitext(video_path)[0] + '.mp3'

        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path, codec='mp3')

        video_clip.close()
        audio_clip.close()

        return audio_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
