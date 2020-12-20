from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager,
		     self).get_queryset()\
                          .filter(status='active')


class DisabledManager(models.Manager):
    def get_queryset(self):
        return super(DisabledManager,
		     self).get_queryset()\
                          .filter(status='disabled')


class Currency(models.Model):
    code = models.CharField(max_length=4)
    slug = models.SlugField(max_length=4)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('tour:currency-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'code',
        )
        verbose_name = _('Currency')
        verbose_name_plural = _('Currency')


class Equipment(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:equipment-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Equipment')
        verbose_name_plural = _('Equipment')


class TravelDocument(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:travel-document-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Travel Document')
        verbose_name_plural = _('Travel Documents')


class PhysicalLevel(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:physical-level-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Physical Level')
        verbose_name_plural = _('Physical Levels')


class DifficultyLevel(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:difficulty-level-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Difficulty Level')
        verbose_name_plural = _('Difficulty Levels')


class Activity(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True)
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
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True)
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
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    continent = models.ForeignKey(Continent, on_delete=models.DO_NOTHING)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True)
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
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, default=1)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True)
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
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True)
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
    name = models.CharField(max_length=250)
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
        default='mountain'
    )
    altitude = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        default=0
    )
    description = models.TextField(blank=True)
    place = models.ManyToManyField(Place)
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
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    tour_object = models.ForeignKey(TourObject, on_delete=models.DO_NOTHING, blank=True, null=True)
    place = models.ManyToManyField(Place)
    description = models.TextField(blank=True)
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


class Touring(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    place = models.ManyToManyField(Place)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:touring-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = _('Touring')
        verbose_name_plural = _('Touring')


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
    name = models.CharField(max_length=250)
    country = models.ForeignKey(Country,on_delete=models.DO_NOTHING, blank=True, null=True)
    birth_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Birthday'),
        verbose_name=_('Birth date')
    )
    about_me = models.TextField(blank=True)
    qualification = models.CharField(
        max_length=20,
        choices=QUALIFICATION_CHOICES,
        default='unqualified'
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
        verbose_name = _('GuideProfile')
        verbose_name_plural = _('GuideProfiles')


class Day(models.Model):
   name = models.CharField(max_length=250)
   interary = models.TextField(blank=True)
   tour = models.ForeignKey('Tour',on_delete=models.CASCADE, default=1)

   def __str__(self):
       return self.name

   def get_absolute_url(self):
       return reverse('tour:day-detail', kwargs={'slug': self.slug})

   class Meta:
       ordering = (
           'name',
       )
       verbose_name = _('Day')
       verbose_name_plural = _('Days')


class Tour(models.Model):
    STATUS_CHOICES = (
        ('disabled', _('Disabled')),
        ('active', _('Active')),
    )
    activity = models.ManyToManyField(Activity)
    tour_object = models.ManyToManyField(TourObject, blank=True)
    route = models.ManyToManyField(Route, blank=True)
    touring = models.ForeignKey(Touring, on_delete=models.DO_NOTHING, null=True, blank=True)
    continent = models.ManyToManyField(Continent, blank=True)
    country = models.ManyToManyField(Country, blank=True)
    region= models.ManyToManyField(Region, blank=True)
    place = models.ManyToManyField(Place)
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='date_created')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(blank=True)
    danger_caution = models.TextField(blank=True)
    typical_weather = models.TextField(blank=True)
    medical_insurance = models.TextField(blank=True)
    responsability = models.TextField(blank=True)
    accomodation = models.TextField(blank=True)
    food = models.TextField(blank=True)
    add_info = models.TextField(blank=True)
    guide = models.ManyToManyField(GuideProfile, blank=True)
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
    time_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    min_altitude_m = models.IntegerField(default=0)
    max_altitude_m = models.IntegerField(default=0)
    altitude_gain_m = models.IntegerField(default=0)
    total_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    equipment_list = models.ManyToManyField(Equipment, blank=True)
    doc_list = models.ManyToManyField(TravelDocument, blank=True)
    difficulty_level = models.ForeignKey(DifficultyLevel, on_delete=models.DO_NOTHING, null=True, blank=True)
    physical_level = models.ForeignKey(PhysicalLevel, on_delete=models.DO_NOTHING, null=True, blank=True)
    client_guide_ratio = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, null=True, blank=True)
    price_include = models.TextField(blank=True)
    price_exclude = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    active = ActiveManager()
    disabled = DisabledManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour:tour-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = (
            '-date_created',
        )
        verbose_name = _('Tour')
        verbose_name_plural = _('Tours')
