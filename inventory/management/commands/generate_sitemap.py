# inventory/management/commands/generate_sitemap.py

import json
import os
from django.core.management.base import BaseCommand
from inventory.models import Location

class Command(BaseCommand):
    help = "Generates a sitemap.json file for all country locations, including sub-locations (states)."

    def handle(self, *args, **kwargs):
        # Fetch all country-level locations
        countries = Location.objects.filter(location_type='country').order_by('title')

        
        sitemap = []

        for country in countries:
            
            sub_locations = Location.objects.filter(country_code=country.country_code, location_type='state').order_by('title')
            
            
            locations_list = []

            for sub_location in sub_locations:
               
                location_slug = sub_location.title.lower().replace(' ', '-')
                locations_list.append({
                    sub_location.title: f"{country.country_code.lower()}/{location_slug}"
                })

            
            country_data = {
                country.title: country.country_code.lower(),
                "locations": locations_list
            }

            sitemap.append(country_data)

       
        sitemap_json = json.dumps(sitemap, indent=4)
        
       
        output_directory = os.path.join(os.getcwd(), 'output')
        os.makedirs(output_directory, exist_ok=True)
        sitemap_path = os.path.join(output_directory, 'sitemap.json')

        with open(sitemap_path, 'w') as json_file:
            json_file.write(sitemap_json)

        self.stdout.write(self.style.SUCCESS('Successfully generated sitemap.json'))
