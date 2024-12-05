# Assignment-6-Django
# Property Management System

This Django-based Property Management System provides an admin interface to manage property information, including locations, accommodations, and geospatial data using PostgreSQL with PostGIS extension for geospatial support.

## Features

- **Property Management**: Manage properties (accommodations) with support for localized descriptions and amenities.
- **Location Management**: Store hierarchical locations (continents, countries, states, cities) with geolocation data.
- **Geospatial Data Handling**: Use PostGIS for handling geospatial data like property and location coordinates.
- **User Registration for Property Owners**: Allow users to sign up as property owners, with admin approval required before activation.
- **Admin Features**: Manage properties, locations, and users via the Django Admin interface, including filters and search options for easy data handling.

## Requirements

- Python 3.12
- Django 4.2.7
- PostgreSQL 15+ with PostGIS extension
- Docker (for PostgreSQL/PostGIS setup)
- GDAL 3.8.1 (for geospatial support)

## Project Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/property-management-system.git
cd Assignment-6-Django-main
```

### Step 2: Set Up the Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Set Up PostgreSQL with PostGIS

Ensure that PostgreSQL is installed with PostGIS enabled. If using Docker, you can set up PostgreSQL and PostGIS with a docker-compose.yml file like:

```bash

services:
  web:
    build: .
    container_name: inventory_management-web
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db

  db:
    image: postgis/postgis:latest
    container_name: inventory_management-db
    environment:
      POSTGRES_DB: inventory_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  db_data:

```
### Step 4: Configure Django Settings

Update the DATABASES settings in inventory_management/settings.py to connect to your PostgreSQL/PostGIS database:

```bash

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',  # Use the PostGIS backend
        'NAME': 'inventory_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',  # Use the service name defined in docker-compose.yml
        'PORT': '5432',
    }
}

```
### Step 5: Run Migrations

```bash
docker-compose exec web python manage.py migrate

```

### Step 6: Load Fixture 

```bash
docker-compose exec web python manage.py loaddata initial_data.json

```

### Step 7: Create a Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### Step 8: Start the Django Development Server

```bash
docker-compose exec web python manage.py runserver 0.0.0.0:8000
```
### Step 9: Access the Django Application

If you've started the server correctly, you can access your Django application from your browser by navigating to:

```bash
http://localhost:8000/
```
For Django Admin:

```bash
http://localhost:8000/admin/
```
You can now manage the application, including creating and editing locations and accommodations, via the Admin interface.


## User Registration
Property owners can register via a custom sign-up form, and their accounts will require admin approval before activation.

## Admin Interface
The Django Admin panel is customized for managing users, locations, accommodations, and their localized versions:

- LocationAdmin: Manage locations with filters by location type, country code, etc.
- AccommodationAdmin: Manage properties with filters by country, bedroom count, and publication status.

## Additional Notes
- The user approval system is managed via the Django Admin interface. Admins can approve pending users by marking them as active.
- Initial data for locations should be added via the Django Admin or a custom management script.

## License
This project is open-source under the MIT License.
