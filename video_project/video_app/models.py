
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    subtitle_path = models.CharField(max_length=255, null=True, blank=True)  # For search
    subtitle_url = models.CharField(max_length=255, null=True, blank=True)  # For captions in video


    def __str__(self):
        return self.title

