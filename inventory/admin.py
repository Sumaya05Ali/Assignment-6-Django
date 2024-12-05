from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Location, Accommodation, LocalizeAccommodation


class UserAdmin(BaseUserAdmin):
    list_filter = ('is_active',)  # Add a filter for user status
    list_display = ('username', 'email', 'is_active')

    def get_queryset(self, request):
        
        return super().get_queryset(request)

    actions = ['approve_user']

    def approve_user(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, 'Selected users have been approved.')
    approve_user.short_description = 'Approve selected users'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register Property Owners Group
property_owners_group, created = Group.objects.get_or_create(name='Property Owners')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at')
    search_fields = ('title', 'city', 'state_abbr', 'country_code')
    list_filter = ('location_type', 'country_code')

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('title', 'country_code', 'bedroom_count', 'review_score', 'usd_rate', 'published', 'created_at')
    search_fields = ('title', 'country_code', 'location__title')
    list_filter = ('country_code', 'bedroom_count', 'published')
    raw_id_fields = ('location', 'user')

@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('property', 'language', 'description')
    search_fields = ('property__title', 'language')