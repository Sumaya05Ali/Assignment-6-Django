from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from .models import Location, Accommodation, LocalizeAccommodation

class LocationModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            title="Test Location in New York City",
            center=Point(-74.0060, 40.7128),
            location_type="metropolitan city",
            country_code="US",
            state_abbr="NY",
            city="New York City"
        )

    def test_location_creation(self):
        self.assertEqual(self.location.title, "Test Location in New York City")
        self.assertEqual(self.location.center.x, -74.0060)  # Longitude
        self.assertEqual(self.location.center.y, 40.7128)  # Latitude
        self.assertEqual(self.location.location_type, "metropolitan city")
        self.assertEqual(self.location.country_code, "US")

    def test_location_optional_fields(self):
        location_minimal = Location.objects.create(
            title="Minimal Location",
            center=Point(0, 0),
            location_type="minimal",
            country_code="XX"
        )
        self.assertIsNone(location_minimal.state_abbr)
        self.assertIsNone(location_minimal.city)

class AccommodationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.location = Location.objects.create(
            title="Test Location in New York City",
            center=Point(-74.0060, 40.7128),
            location_type="metropolitan city",
            country_code="US",
            state_abbr="NY",
            city="New York City"
        )
        self.accommodation = Accommodation.objects.create(
            title="Luxurious Downtown New York Apartment",
            feed=1,
            country_code="US",
            bedroom_count=2,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(-74.0060, 40.7128),
            location=self.location,
            user=self.user,
            amenities={"wifi": True, "parking": True, "kitchen": True},
            images=["main_image.jpg", "living_room.jpg", "bedroom.jpg"]
        )

    def test_accommodation_creation(self):
        self.assertEqual(self.accommodation.title, "Luxurious Downtown New York Apartment")
        self.assertEqual(self.accommodation.bedroom_count, 2)
        self.assertEqual(self.accommodation.review_score, 4.5)
        self.assertFalse(self.accommodation.published)  # Default is False

    def test_accommodation_json_fields(self):
        self.assertTrue(self.accommodation.amenities.get("wifi"))
        self.assertEqual(len(self.accommodation.images), 3)

class LocalizeAccommodationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.location = Location.objects.create(
            title="Test Location in New York City",
            center=Point(-74.0060, 40.7128),
            location_type="metropolitan city",
            country_code="US",
            state_abbr="NY",
            city="New York City"
        )
        self.accommodation = Accommodation.objects.create(
            title="Luxurious Downtown New York Apartment",
            feed=1,
            country_code="US",
            bedroom_count=2,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(-74.0060, 40.7128),
            location=self.location,
            user=self.user,
            amenities={"wifi": True, "parking": True, "kitchen": True},
            images=["main_image.jpg", "living_room.jpg", "bedroom.jpg"]
        )
        self.localized_accommodation = LocalizeAccommodation.objects.create(
            property=self.accommodation,
            language="en",
            description="A beautiful and spacious apartment located in the heart of downtown New York City, perfect for travelers and professionals.",
            policy={"check_in": "2:00 PM", "check_out": "11:00 AM", "extra_details": "Late check-in available upon request"}
        )

    def test_localized_accommodation_creation(self):
        self.assertEqual(self.localized_accommodation.description, "A beautiful and spacious apartment located in the heart of downtown New York City, perfect for travelers and professionals.")
        self.assertEqual(self.localized_accommodation.policy["check_in"], "2:00 PM")
        self.assertEqual(self.localized_accommodation.language, "en")

    def test_multiple_localizations(self):
        # Test that multiple localizations can be created for same accommodation
        LocalizeAccommodation.objects.create(
            property=self.accommodation,
            language="es",
            description="Un hermoso y espacioso apartamento ubicado en el corazón del centro de Nueva York, perfecto para viajeros y profesionales.",
            policy={"check_in": "14:00", "check_out": "11:00", "extra_details": "Check-in tardío disponible con solicitud"}
        )
        localizations = LocalizeAccommodation.objects.filter(property=self.accommodation)
        self.assertEqual(localizations.count(), 2)
