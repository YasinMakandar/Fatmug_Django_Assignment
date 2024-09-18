import subprocess
import os
from django.conf import settings

def extract_subtitles(video_path, output_path):
    try:
        # Command to extract subtitles using ffmpeg
        command = [
            'ffmpeg', '-i', video_path, 
            '-map', '0:s:0',  # First subtitle stream
            os.path.join(output_path, 'subtitles.srt')
        ]
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
