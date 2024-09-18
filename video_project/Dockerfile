# Use the official Python image from the Docker Hub
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run the server
CMD ["gunicorn", "video_project.wsgi:application", "--bind", "0.0.0.0:8000"]
