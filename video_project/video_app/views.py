from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from .forms import VideoUploadForm

import os
from django.conf import settings
from .utils import extract_subtitles
from .models import Video
import re
import logging
from datetime import timedelta

# Video upload view
def video_upload(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()  # Save the uploaded video

            # Start subtitle extraction process
            video_path = os.path.join(settings.MEDIA_ROOT, video.video_file.name)
            output_path = os.path.join(settings.MEDIA_ROOT, 'subtitles', video.title)
            os.makedirs(output_path, exist_ok=True)

            success = extract_subtitles(video_path, output_path)
            if success:
                # Absolute path for server-side usage (search)
                subtitle_file_abs_path = os.path.join(output_path, 'subtitles.vtt')

                # Public path for video captions (accessible via browser)
                subtitle_file_public_path = os.path.join(settings.MEDIA_URL, 'subtitles', video.title, 'subtitles.vtt')

                # Save both paths for different purposes
                video.subtitle_path = subtitle_file_abs_path  # For search (absolute path)
                video.subtitle_url = subtitle_file_public_path  # For captions (URL for video player)
                video.save()

            return redirect('video_list')  # Redirect to a list view after upload
    else:
        form = VideoUploadForm()
    return render(request, 'video_upload.html', {'form': form})


# Subtitle search view



import re
from django.shortcuts import render, get_object_or_404
from .models import Video
import logging

logger = logging.getLogger(__name__)

def time_to_seconds(time_str):
    """Convert subtitle timestamp (HH:MM:SS,ms or MM:SS.ms) to seconds."""
    try:
        parts = time_str.replace(',', '.').split(':')
        if len(parts) == 2:
            return float(parts[0]) * 60 + float(parts[1])
        elif len(parts) == 3:
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        else:
            logger.error(f"Invalid time format: {time_str}")
            return 0
    except ValueError:
        logger.error(f"Invalid time format: {time_str}")
        return 0

def parse_subtitle_block(block):
    lines = block.strip().split('\n')
    if len(lines) < 2:
        return None

    # Try to find the timestamp line
    timestamp_line = None
    for line in lines:
        if ' --> ' in line:
            timestamp_line = line
            break

    if not timestamp_line:
        return None

    # Extract text
    text_lines = [line for line in lines if line != timestamp_line and not line.isdigit()]
    subtitle_text = ' '.join(text_lines)

    # Extract start time
    start_time = timestamp_line.split(' --> ')[0]

    return {
        'start_time': start_time,
        'seconds': time_to_seconds(start_time),
        'subtitle_text': subtitle_text
    }

def search_subtitles(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    query = request.GET.get('q', '').strip().lower()
    results = []

    if query and video.subtitle_path:
        try:
            with open(video.subtitle_path, 'r', encoding='utf-8') as f:
                subtitles = f.read()
        except FileNotFoundError:
            logger.error(f"Subtitle file not found: {video.subtitle_path}")
            return render(request, 'search_results.html', {'video': video, 'query': query, 'results': [], 'error': 'Subtitle file not found.'})

        # Split subtitles into blocks
        subtitle_blocks = re.split(r'\n\n+', subtitles.strip())

        for block in subtitle_blocks:
            parsed_block = parse_subtitle_block(block)
            if parsed_block and query in parsed_block['subtitle_text'].lower():
                results.append(parsed_block)

    # Sort results by time
    results.sort(key=lambda x: x['seconds'])

    return render(request, 'search_results.html', {'video': video, 'query': query, 'results': results})

# Video list view
def video_list(request):
    videos = Video.objects.all()  # Fetch all videos
    return render(request, 'video_list.html', {'videos': videos})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'video_detail.html', {'video': video})

# Updated extract_subtitles function
def extract_subtitles(video_path, output_path):
    subtitle_file = os.path.join(output_path, "subtitles.vtt")
    os.makedirs(output_path, exist_ok=True)  # Ensure the output directory exists
    os.system(f"ffmpeg -i {video_path} -map 0:s:0 {subtitle_file}")

    # Log or print the subtitle file path
    logger.debug(f"Subtitle file created at: {subtitle_file}")
    print(f"Subtitle file created at: {subtitle_file}")

    return subtitle_file
