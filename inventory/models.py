from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
import uuid

class Location(models.Model):
    id = models.CharField(primary_key=True, max_length=20, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    center = gis_models.PointField()  # PostGIS point for geolocation
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_locations')
    location_type = models.CharField(max_length=50)  
    country_code = models.CharField(max_length=2)
    state_abbr = models.CharField(max_length=3, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Accommodation(models.Model):
    id = models.CharField(primary_key=True, max_length=20, default=uuid.uuid4, editable=False)
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=200)
    country_code = models.CharField(max_length=2)
    bedroom_count = models.PositiveIntegerField()
    review_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    center = gis_models.PointField()
    images = models.JSONField(default=list)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    amenities = models.JSONField(default=dict)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class LocalizeAccommodation(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    language = models.CharField(max_length=2)
    description = models.TextField()
    policy = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.property.title} - {self.language}"
