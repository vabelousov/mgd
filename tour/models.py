from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager,
                     self).get_queryset().filter(status='active')


class DisabledManager(models.Manager):
    def get_queryset(self):
        return super(DisabledManager,
                     self).get_queryset().filter(status='disabled')


class Vocabulary(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    def __str__(self):
        return self.name


class Equipment(Vocabulary):
    EQUIP_CHOICES = (
        ('closes', _('Closes')),
        ('equip', _('Equipment')),
        ('rent', _('From rentals')),
    )
    vocabulary_type = 'equipment'
    equipment_type = models.CharField(
        max_length=6,
        choices=EQUIP_CHOICES,
        default='equip'
    )

    class Meta:
        ordering = (
            'equipment_type',
            'name',
        )
        verbose_name = _('Equipment')
        verbose_name_plural = _('Equipment')


class TravelDocument(Vocabulary):
    vocabulary_type = 'travel_document'

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')


class PhysicalLevel(Vocabulary):
    vocabulary_type = 'physical_level'

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Physical Level')
        verbose_name_plural = _('Physical Levels')


class DifficultyLevel(Vocabulary):
    vocabulary_type = 'difficulty_level'

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Difficulty Level')
        verbose_name_plural = _('Difficulty Levels')


class Currency(models.Model):
    code = models.CharField(max_length=4, verbose_name=_('Code'))
    slug = models.SlugField(max_length=4)
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    def __str__(self):
        return self.code

    class Meta:
        ordering = (
            'code',
        )
        verbose_name = _('Currency')
        verbose_name_plural = _('Currency')


class Activity(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:activity-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')


class Continent(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:continent-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Continent')
        verbose_name_plural = _('Continents')


class Country(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    continent = models.ForeignKey(Continent, on_delete=models.SET_NULL, null=True, verbose_name=_('Continent'))
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:country-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'continent',
            'name',
        )
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class Region(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, verbose_name=_('Country'))
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:region-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'country',
        )
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')


class Place(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name=_('Region'))
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:place-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'region',
        )
        verbose_name = _('Place')
        verbose_name_plural = _('Places')


class Refuge(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name=_('Region'))
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    altitude = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        verbose_name=_('Altitude')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    web_link = models.URLField(
        null=True, blank=True, verbose_name=_('Web link')
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:refuge-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'region',
        )
        verbose_name = _('Refuge')
        verbose_name_plural = _('Refuges')


class TourObject(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    OBJECT_TYPE_CHOICES = (
        ('mountain', _('Mountain')),
        ('col', _('Col, Pass')),
        ('crag', _('Crag')),
        ('icefall', _('Icefall')),
        ('slope', _('Slope')),
    )
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    object_type = models.CharField(
        max_length=10,
        choices=OBJECT_TYPE_CHOICES,
        default='mountain',
        verbose_name=_('Object type')
    )
    altitude = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        verbose_name=_('Altitude')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    place = models.ManyToManyField(Place, verbose_name=_('Place'))
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:tour-object-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            '-altitude',
        )
        verbose_name = _('Tour Object')
        verbose_name_plural = _('Tour Objects')


class Route(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    tour_object = models.ForeignKey(
        TourObject,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_('Tour Object')
    )
    place = models.ManyToManyField(Place, verbose_name=_('Place'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:route-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'tour_object',
        )
        verbose_name = _('Route')
        verbose_name_plural = _('Routes')


class GuideProfile(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    QUALIFICATION_CHOICES = (
        ('unqualified', _('Unqualified')),
        ('instructor', _('Instructor')),
        ('national-aspirant', _('National aspirant')),
        ('national-guide', _('National guide')),
        ('ifmga-aspirant', _('IFMGA aspirant')),
        ('ifmga-guide', _('IFMGA/UIAGM guide')),
    )
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Country'))
    birth_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Birth date'),
        verbose_name=_('Birth date')
    )
    about_me = models.TextField(blank=True, verbose_name=_('About me'))
    qualification = models.CharField(
        max_length=20,
        choices=QUALIFICATION_CHOICES,
        default='unqualified',
        verbose_name=_('Qualification')
    )
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:guide-profile', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            '-date_created',
        )
        verbose_name = _('Guide Profile')
        verbose_name_plural = _('Guide Profiles')


class Day(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    interary = models.TextField(blank=True, verbose_name=_('Interary'))
    ascent = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        verbose_name=_('Ascent')
    )
    descent = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        verbose_name=_('Descent')
    )
    ascent_time_minutes = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        verbose_name=_('Ascent time')
    )
    descent_time_minutes = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        verbose_name=_('Descent time')
    )
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, default=1, verbose_name=_('Tour'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:day-detail', kwargs={'slug': self.name})

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Day')
        verbose_name_plural = _('Days')


class Participant(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    calendar_event = models.ForeignKey('Calendar', on_delete=models.CASCADE, default=1, verbose_name=_('Calendar'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:participant-detail', kwargs={'slug': self.name})

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')


class Calendar(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, default=1, verbose_name=_('Tour'))
    start_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Date from'),
        verbose_name=_('Date from')
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Date through'),
        verbose_name=_('Date through')
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        period = str(self.start_date)+' - '+str(self.end_date)
        if period == '-':
            period = _('by demand')
        return self.tour.name+'-['+period+']'

    def get_availability(self):
        guide_cnt = self.tour.guide.count()
        return guide_cnt*self.tour.client_guide_ratio-Participant.objects.filter(calendar_event__exact=self.pk).count()

    class Meta:
        ordering = (
            'tour',
            '-start_date',
        )
        verbose_name = _('Calendar Event')
        verbose_name_plural = _('Calendar Events')


class PriceOption(models.Model):
    LIST_TYPE_CHOICES = (
        ('includes', _('Includes')),
        ('excludes', _('Excludes')),
    )
    name = models.CharField(max_length=1000, verbose_name=_('Name'))
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, default=1, verbose_name=_('Tour'))
    list_type = models.CharField(
        max_length=10,
        choices=LIST_TYPE_CHOICES,
        default='excludes'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:price-option', kwargs={'slug': self.name})

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Price option')
        verbose_name_plural = _('Price options')


class TourEvent(models.Model):
    EVENT_TYPE_CHOICES = (
        ('ascent', _('Ascent')),
        ('acclimatization', _('Acclimatization')),
    )
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, default=1, verbose_name=_('Tour'))
    tour_object = models.ForeignKey('TourObject', on_delete=models.CASCADE, default=1, verbose_name=_('Tour Object'))
    route = models.ForeignKey('Route', on_delete=models.CASCADE, default=1, verbose_name=_('Route'))
    event_type = models.CharField(
        max_length=15,
        choices=EVENT_TYPE_CHOICES,
        default='ascent'
    )
    event_index = models.IntegerField(default=0, verbose_name=_('Event Index'))

    def __str__(self):
        return self.tour.name+' '+self.tour_object.name+' '+self.route.name

    def get_absolute_url(self):
        return reverse('tour:tour-event', kwargs={'pk': self.pk})

    class Meta:
        ordering = (
            'event_index',
        )
        verbose_name = _('Tour Event')
        verbose_name_plural = _('Tour Events')


class Tour(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    activity = models.ManyToManyField(Activity, verbose_name=_('Activity'))
    continent = models.ManyToManyField(Continent, blank=True, verbose_name=_('Continent'))
    country = models.ManyToManyField(Country, blank=True, verbose_name=_('Country'))
    region = models.ManyToManyField(Region, blank=True, verbose_name=_('Region'))
    place = models.ManyToManyField(Place, verbose_name=_('Place'))
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    danger_caution = models.TextField(blank=True, verbose_name=_('Danger caution'))
    typical_weather = models.TextField(blank=True, verbose_name=_('Weather'))
    medical_insurance = models.TextField(blank=True, verbose_name=_('Insurance'))
    responsability = models.TextField(blank=True, verbose_name=_('Resposability'))
    refuge = models.ManyToManyField(Refuge, blank=True, verbose_name=_('Refuge'))
    accomodation = models.TextField(blank=True, verbose_name=_('Accomodation'))
    food = models.TextField(blank=True, verbose_name=_('Food'))
    add_info = models.TextField(blank=True, verbose_name=_('Add. Info'))
    rental = models.TextField(blank=True, verbose_name=_('Rental'))
    transport = models.TextField(blank=True, verbose_name=_('Transport'))
    guide = models.ManyToManyField(GuideProfile, blank=True, verbose_name=_('Guide Profile'))
    equipment_list = models.ManyToManyField(Equipment, blank=True, verbose_name=_('Equipment'))
    travel_documents = models.ManyToManyField(TravelDocument, blank=True, verbose_name=_('Documents'))
    difficulty_level = models.ForeignKey(
        DifficultyLevel,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Difficulty Level')
    )
    physical_level = models.ForeignKey(
        PhysicalLevel,
        on_delete=models.SET_NULL,
        null=True, blank=True,verbose_name=_('Physical Level')
    )
    client_guide_ratio = models.IntegerField(default=1, verbose_name=_('Guide-Client ratio'))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_('Price'))
    show_price = models.BooleanField(verbose_name=_('Show price'), default=True)
    allow_booking = models.BooleanField(verbose_name=_('Allow booking'), default=True)
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Currency')
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:tour-detail', kwargs={'slug': self.slug})

    def get_days_count(self):
        return Day.objects.filter(tour__pk=self.pk).count()

    class Meta:
        ordering = (
            '-date_created',
        )
        verbose_name = _('Tour')
        verbose_name_plural = _('Tours')
