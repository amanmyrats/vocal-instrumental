# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies for libsndfile
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get install -y autoconf autogen automake build-essential libasound2-dev \
                       libflac-dev libogg-dev libtool libvorbis-dev libopus-dev \
                       libmp3lame-dev libmpg123-dev pkg-config python3

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose the port that Django will run on
EXPOSE 8000

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
