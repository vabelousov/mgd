from django.db import models
from django.db.models import Max, Min
from django.urls import reverse
import itertools
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch import receiver


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


class LegalObject(Vocabulary):
    LEGAL_CHOICES = (
        ('danger', _('Dangers')),
        ('safety', _('Safety')),
        ('insurance', _('Insurance'))
    )
    vocabulary_type = 'legal'
    legal_type = models.CharField(
        max_length=10,
        choices=LEGAL_CHOICES,
        default='danger'
    )
    objects = models.Manager()

    class Meta:
        ordering = (
            'legal_type',
            'name',
        )
        verbose_name = _('Legal Object')
        verbose_name_plural = _('Legal Objects')


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

    objects = models.Manager()

    class Meta:
        ordering = (
            'equipment_type',
            'name',
        )
        verbose_name = _('Equipment')
        verbose_name_plural = _('Equipment')


class TravelDocument(Vocabulary):
    vocabulary_type = 'travel_document'

    objects = models.Manager()

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')


class PhysicalLevel(Vocabulary):
    vocabulary_type = 'physical_level'
    level_index = models.IntegerField(default=0, verbose_name=_('Level Index'))

    objects = models.Manager()

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Physical Level')
        verbose_name_plural = _('Physical Levels')


class DifficultyLevel(Vocabulary):
    vocabulary_type = 'difficulty_level'
    level_index = models.IntegerField(default=0, verbose_name=_('Level Index'))

    objects = models.Manager()

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Difficulty Level')
        verbose_name_plural = _('Difficulty Levels')


class Currency(models.Model):
    code = models.CharField(max_length=4, verbose_name=_('Code'))
    slug = models.SlugField(max_length=4, default='', editable=False)
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    objects = models.Manager()

    def __str__(self):
        return self.code

    def _generate_slug(self):
        value = self.code
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Currency.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

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
    slug = models.SlugField(max_length=250, default='', editable=False, unique_for_date='date_created')
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

    def _generate_slug(self):
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Currency.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

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
    slug = models.SlugField(max_length=250, default='', editable=False, unique_for_date='date_created')
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

    def _generate_slug(self):
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Currency.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

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
    slug = models.SlugField(max_length=250, default='', editable=False, unique_for_date='date_created')
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

    def _generate_slug(self):
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Currency.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

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
    slug = models.SlugField(max_length=250, default='', editable=False, unique_for_date='date_created')
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

    def _generate_slug(self):
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Currency.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

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
    slug = models.SlugField(max_length=250, default='', editable=False, unique_for_date='date_created')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name=_('Region'))
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    altitude = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        verbose_name=_('Altitude')
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def _generate_slug(self):
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Currency.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

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
    slug = models.SlugField(max_length=250, default='', editable=False, unique_for_date='date_created')
    #  ??? как увязать приют в место, район и тд. сейчас через маршрут
    default_place = models.ManyToManyField(Place, verbose_name=_('Place by default'))
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

    def _generate_slug(self):
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Currency.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tour:refuge-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'name',
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
    slug = models.SlugField(max_length=250, default='', editable=False, unique_for_date='date_created')
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
    # ???? как увязать гору в место, район и тд. сейчас через маршрут
    default_place = models.ManyToManyField(Place, verbose_name=_('Place by default'))
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def _generate_slug(self):
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Currency.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tour:tour-object-detail', kwargs={'slug': self.slug})

    def get_routes(self):
        return Route.active.filter(tour_object__exact=self)

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
    description = models.TextField(blank=True, verbose_name=_('Description'))
    slug = models.SlugField(max_length=250, default='', editable=False, unique_for_date='date_created')
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
    activity = models.ManyToManyField(Activity, verbose_name=_('Activity'))
    place = models.ManyToManyField(Place, verbose_name=_('Place'))
    refuge = models.ManyToManyField(Refuge, blank=True, verbose_name=_('Refuge'))
    equipment_list = models.ManyToManyField(Equipment, blank=True, verbose_name=_('Equipment'))
    difficulty_level = models.ForeignKey(
        DifficultyLevel,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Difficulty Level')
    )
    physical_level = models.ForeignKey(
        PhysicalLevel,
        on_delete=models.SET_NULL,
        null=True, blank=True, verbose_name=_('Physical Level')
    )
    client_guide_ratio = models.IntegerField(default=1, verbose_name=_('Guide-Client ratio'))
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def _generate_slug(self):
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Currency.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

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
    slug = models.SlugField(max_length=250, default='', editable=False, unique_for_date='date_created')
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

    def _generate_slug(self):
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Currency.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

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
    morning_altitude = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        verbose_name=_('Morning Alti')
    )
    day_altitude = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        verbose_name=_('Day Alti')
    )
    night_altitude = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0,
        verbose_name=_('Night Alti')
    )
    day_index = models.IntegerField(default=0, verbose_name=_('Day Index'))
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, default=1, verbose_name=_('Tour'))

    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:day-detail', kwargs={'slug': self.name})

    class Meta:
        ordering = (
            'day_index',
            'name'
        )
        verbose_name = _('Day')
        verbose_name_plural = _('Days')


class Participant(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    calendar_event = models.ForeignKey('Calendar', on_delete=models.CASCADE, default=1, verbose_name=_('Calendar'))

    objects = models.Manager()

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


class PriceValue(models.Model):
    group = models.IntegerField(default=1, verbose_name=_('group'))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name=_('Price'))
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, default=1, verbose_name=_('Tour'))

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if self.tour.price > self.price or self.tour.price == 0:
            Tour.objects.update_or_create(id=self.tour.pk, defaults={"price": self.price})
        super().save(*args, **kwargs)

    class Meta:
        ordering = (
            'tour',
            'group'
        )
        verbose_name = _('Price value')
        verbose_name_plural = _('Price values')


class Calendar(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('canceled', _('Canceled')),
        ('done', _('Done')),
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
    note = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Notice'))
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
        period = str(self.start_date)+' - '+str(self.end_date)
        if period == '-':
            period = _('by demand')
        return self.tour.name+'-['+period+']'

    def get_availability(self):
        guide_cnt = self.tour.guide.count()
        return guide_cnt*self.tour.get_guide_client_ratio()-Participant.objects.filter(
            calendar_event__exact=self.pk
        ).count()

    class Meta:
        ordering = (
            'start_date',
            'tour',
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

    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:price-option', kwargs={'slug': self.name})

    class Meta:
        ordering = (
            '-list_type',
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

    objects = models.Manager()

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
    name = models.CharField(max_length=250, verbose_name=_('Name'))
    slug = models.SlugField(max_length=250, default='', editable=False, unique_for_date='date_created')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))  # change to text-block-model
    guide = models.ManyToManyField(GuideProfile, blank=True, verbose_name=_('Guide Profile'))
    danger = models.ForeignKey(
        LegalObject,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Danger Caution'),
        related_name='danger'
    )
    insurance = models.ForeignKey(
        LegalObject,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Medical Insurance'),
        related_name='insurance'
    )
    safety = models.ForeignKey(
        LegalObject,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_('Safety'),
        related_name='safety'
    )
    travel_documents = models.ManyToManyField(TravelDocument, blank=True, verbose_name=_('Documents'))
    typical_weather = models.TextField(blank=True, verbose_name=_('Weather'))
    season = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('Season'))
    accomodation = models.TextField(blank=True, verbose_name=_('Accomodation'))
    food = models.TextField(blank=True, verbose_name=_('Food'))
    add_info = models.TextField(blank=True, verbose_name=_('Add. Info'))
    rental = models.TextField(blank=True, verbose_name=_('Rental'))
    transport = models.TextField(blank=True, verbose_name=_('Transport'))
    '''
    price - обновляется из PriceValue автоматически, его не нужно вводить руками
    '''
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

    def _generate_slug(self):
        value = self.name
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Currency.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tour:tour-detail', kwargs={'slug': self.slug})

    def get_days_count(self):
        return Day.objects.filter(tour__pk=self.pk).count()

    def get_activities(self):
        return Activity.active.filter(
            route__in=Route.active.filter(
                tourevent__in=TourEvent.objects.filter(tour__exact=self)
            )
        ).distinct()

    def get_refuges(self):
        return Refuge.active.filter(
            route__in=Route.active.filter(
                tourevent__in=TourEvent.objects.filter(tour__exact=self)
            )
        ).distinct()

    def get_main_tour_objects(self):
        return TourObject.active.filter(
            route__in=Route.active.filter(
                tourevent__in=TourEvent.objects.filter(tour__exact=self, event_type__exact='ascent')
            )
        ).distinct()

    def get_secondary_tour_objects(self):
        return TourObject.active.filter(
            route__in=Route.active.filter(
                tourevent__in=TourEvent.objects.filter(tour__exact=self, event_type__exact='acclimatization')
            )
        ).distinct()

    def get_tour_object_route(self, tour_object):
        return Route.active.get(
                tourevent__in=TourEvent.objects.filter(tour__exact=self, tour_object__exact=tour_object)
            )

    def get_places(self):
        return Place.active.filter(
            route__in=Route.active.filter(
                tourevent__in=TourEvent.objects.filter(tour__exact=self)
            )
        ).distinct()

    def get_regions(self):
        return Region.active.filter(
            place__in=Place.active.filter(
                route__in=Route.active.filter(
                    tourevent__in=TourEvent.objects.filter(tour__exact=self)
                )
            )
        ).distinct()

    def get_countries(self):
        return Country.active.filter(
            region__in=Region.active.filter(
                place__in=Place.active.filter(
                    route__in=Route.active.filter(
                        tourevent__in=TourEvent.objects.filter(tour__exact=self)
                    )
                )
            )
        ).distinct()

    def get_continents(self):
        return Continent.active.filter(
            country__in=Country.active.filter(
                region__in=Region.active.filter(
                    place__in=Place.active.filter(
                        route__in=Route.active.filter(
                            tourevent__in=TourEvent.objects.filter(tour__exact=self)
                        )
                    )
                )
            )
        ).distinct()

    def get_difficulty_level(self):
        max_index = DifficultyLevel.objects.filter(
            route__in=Route.active.filter(tourevent__in=TourEvent.objects.filter(tour__exact=self))
        ).aggregate(Max('level_index'))['level_index__max']
        return DifficultyLevel.objects.filter(level_index__exact=max_index).first()

    def get_physical_level(self):
        max_index = PhysicalLevel.objects.filter(
            route__in=Route.active.filter(tourevent__in=TourEvent.objects.filter(tour__exact=self))
        ).aggregate(Max('level_index'))['level_index__max']
        return PhysicalLevel.objects.filter(level_index__exact=max_index).first()

    def get_guide_client_ratio(self):
        return Route.active.filter(
            tourevent__in=TourEvent.objects.filter(tour__exact=self)
        ).aggregate(Min('client_guide_ratio'))['client_guide_ratio__min']

    def get_equipment_list(self):
        return Equipment.objects.filter(
            route__in=Route.active.filter(
                tourevent__in=TourEvent.objects.filter(tour__exact=self)
            )
        ).distinct()

    def get_alti_data_plot(self):
        alti = []
        for i, d in enumerate(self.day_set.all().order_by('day_index')):
            if i == 0:
                alti.append(float(d.morning_altitude))
            alti.append(float(d.day_altitude))
            alti.append(float(d.night_altitude))
        return alti

    def get_days_data_plot(self):
        days = []
        d_count = 0
        for i, d in enumerate(self.day_set.all().order_by('day_index')):
            if i == 0:
                days.append(0)
            days.append(d_count+0.5)
            days.append(d_count+1)
            d_count = d_count+1
        return days

    class Meta:
        ordering = (
            '-date_created',
        )
        verbose_name = _('Tour')
        verbose_name_plural = _('Tours')


@receiver(pre_delete, sender=PriceValue)
def update_tour_price(sender, instance, **kwargs):
    min_price = PriceValue.objects.filter(tour=instance.tour).exclude(pk=instance.pk).aggregate(Min('price'))['price__min']
    Tour.objects.update_or_create(id=instance.tour.pk, defaults={"price": min_price})