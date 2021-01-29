from django.contrib import admin
from .models import Activity, Continent, Country, Tour, \
    Region, Place, TourObject, Route, Refuge, \
    GuideProfile, Currency, Day, Equipment, TravelDocument,\
    PhysicalLevel, DifficultyLevel, Participant, Calendar, PriceOption, TourEvent


class TourEventInline(admin.TabularInline):
    model = TourEvent
    extra = 0
    max_num = 100
    classes = ['collapse']


class CalendarInline(admin.TabularInline):
    model = Calendar
    extra = 0
    max_num = 100
    classes = ['collapse']


class PriceOptionInline(admin.TabularInline):
    model = PriceOption
    extra = 0
    max_num = 100
    classes = ['collapse']


class DayInline(admin.TabularInline):
    model = Day
    extra = 0
    max_num = 100
    classes = ['collapse']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'calendar_event')
    list_filter = ('name', 'calendar_event',)
    search_fields = ('name', 'calendar_event')


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('code', 'name',)
    search_fields = ('code', 'name')


@admin.register(Refuge)
class RefugeAdmin(admin.ModelAdmin):
    list_display = ('name', 'altitude', 'description')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'equipment_type')
    list_filter = ('name', 'equipment_type',)
    search_fields = ('name',)


@admin.register(PhysicalLevel)
class PhysicalLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(TravelDocument)
class TravelDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'status', 'date_created')
    list_filter = ('status',)
    search_fields = ('name', 'description')


@admin.register(Continent)
class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'status', 'get_countries', 'date_created')
    list_filter = ('status',)
    search_fields = ('name', 'description')

    def get_countries(self, obj):
        return Country.objects.filter(continent=obj).count()


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'continent', 'get_regions', 'status', 'date_created')
    list_filter = ('status',)
    search_fields = ('name', 'description')

    def get_regions(self, obj):
        return Region.objects.filter(country=obj).count()


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'country', 'get_places', 'status', 'date_created')
    list_filter = ('status',)
    search_fields = ('name', 'description')

    def get_places(self, obj):
        return Place.objects.filter(region=obj).count()


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'region', 'status', 'date_created')
    list_filter = ('status',)
    search_fields = ('name', 'description')


@admin.register(TourObject)
class TourObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'altitude', 'status', 'date_created')
    list_filter = ('status',)
    search_fields = ('name', 'description')
    filter_horizontal = ('place',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "place":
            kwargs["queryset"] = Place.objects.filter(status='active')
        return super(TourObjectAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'tour_object', 'status', 'date_created')
    list_filter = ('status', 'tour_object')
    search_fields = ('name', 'description')
    filter_horizontal = ('place',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "place":
            kwargs["queryset"] = Place.objects.filter(status='active')
        return super(RouteAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    inlines = [DayInline, CalendarInline, PriceOptionInline, TourEventInline]
    list_display = ('name', 'pk', 'get_activities', 'status', 'date_created')
    list_filter = ('status',)
    search_fields = ('name',)
    filter_horizontal = ('activity', 'continent', 'country',
                         'region', 'place', 'guide', 'equipment_list', 'travel_documents', 'refuge')

    def get_activities(self, obj):
        return "\n".join([act.name for act in obj.activity.all()])

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "activity":
            kwargs["queryset"] = Activity.objects.filter(status='active')
        if db_field.name == "place":
            kwargs["queryset"] = Place.objects.filter(status='active')
        return super(TourAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(GuideProfile)
class GuideProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'qualification', 'birth_date', 'status')
    list_filter = ('qualification', 'country')
    search_fields = ('name', 'slug', 'qualification', 'country')
