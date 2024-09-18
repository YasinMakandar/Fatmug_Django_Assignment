# Fatmug_Django_Assignment
 This is django assignment for backend developer position at Fatmug.

 This project is a web application that allows users to upload videos, automatically extract subtitles, and provide a searchable interface for the video content.

## Features

Video upload and processing
Automatic subtitle extraction using ffmpeg
Search functionality within video subtitles
List view of uploaded videos
Multi-language subtitle support
Docker containerization for easy setup and deployment

## Tech Stack

Backend: Django
Database: PostgreSQL
Containerization: Docker
Subtitle Extraction: ffmpeg

Setup

1) Clone the repository:
```
git clone https://github.com/YasinMakandar/Fatmug_Django_Assignment.git
cd video_project

```
2) Build and start the Docker containers:

```
docker-compose up --build
```

3)Apply database migrations:

```
docker-compose exec web python manage.py migrate
```

4) Create a superuser:
```
docker-compose exec web python manage.py createsuperuser
```

5) Access the application at http://localhost:8000


## Usage

a)Upload a video file through the web interface.
b)Wait for the video to be processed and subtitles extracted.
c)View the list of uploaded videos.
d)Select a video to view its details and search within its subtitles.
e)Use the search functionality to find specific phrases within the video.
f)Click on search results to jump to specific timestamps in the video.

## Screenshots
Screenshots of the application in use can be found in the screenshots folder.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License.
