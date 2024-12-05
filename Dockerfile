# Use the official Python 3.12-slim image as base
FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# Install dependencies for PostGIS and GDAL
RUN apt-get update \
    && apt-get install -y \
        postgis \
        gdal-bin \
        python3-gdal \
        build-essential \
        libpq-dev \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Install dependencies
 COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

ENV CPLUS_+INCLUDE_PATH =/usr/include/gdal
ENV C_INCLUDE_PATH =/usr/include/gdal
ENV GDAL_LIBRARY_PATH =/usr/lib/libgdal.so
# Expose port 8000 for the web service
EXPOSE 8000

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
