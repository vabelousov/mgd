from django.contrib import admin
from .models import Activity, Continent, Country, \
    Region, Place, TourObject, Route, Touring, Tour, \
    GuideProfile, Currency, Day, Equipment, TravelDocument, PhysicalLevel, DifficultyLevel, Participant
#, Vocabulary


# @admin.register(Vocabulary)
# class VocabularyAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     list_filter = ('name',)
#     search_fields = ('name',)


class DayInline(admin.TabularInline):
    model = Day
    extra = 0
    max_num = 100
    classes = ['collapse']


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0
    max_num = 30
    classes = ['collapse']


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    list_filter = ('code', 'name',)
    search_fields = ('code', 'name')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
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


@admin.register(Touring)
class TouringAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk', 'status', 'date_created')
    list_filter = ('status',)
    search_fields = ('name', 'description')
    filter_horizontal = ('place',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "place":
            kwargs["queryset"] = Place.objects.filter(status='active')
        return super(TouringAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    inlines = [DayInline, ParticipantInline]
    list_display = ('name', 'start_date', 'end_date', 'pk', 'get_activities', 'status', 'date_created')
    list_filter = ('status',)
    search_fields = ('name',)
    filter_horizontal = ('activity', 'tour_object', 'route', 'continent', 'country',
                         'region', 'place', 'guide', 'equipment_list', 'travel_documents',)

    def get_activities(self, obj):
        return "\n".join([act.name for act in obj.activity.all()])

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "activity":
            kwargs["queryset"] = Activity.objects.filter(status='active')
        if db_field.name == "tour_object":
            kwargs["queryset"] = TourObject.objects.filter(status='active')
        if db_field.name == "route":
            kwargs["queryset"] = Route.objects.filter(status='active')
        if db_field.name == "place":
            kwargs["queryset"] = Place.objects.filter(status='active')
        return super(TourAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(GuideProfile)
class GuideProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'qualification', 'birth_date', 'status')
    list_filter = ('qualification', 'country')
    search_fields = ('name', 'slug', 'qualification', 'country')
