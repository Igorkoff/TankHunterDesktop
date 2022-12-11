from django.conf import settings
from django.utils import timezone
from django.contrib.gis.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

User = settings.AUTH_USER_MODEL


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """ Create and Save a User with the given Email and Password. """
        if not email:
            raise ValueError('Users must have an Email Address.')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """ Create and Save a Staff User with the given Email and Password. """
        user = self.create_user(email=email, password=password)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """ Create and Save a Super User with the given Email and Password. """
        user = self.create_user(email=email, password=password)
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email Address', max_length=255, unique=True, null=False, blank=False)
    first_name = models.CharField(verbose_name='First Name', max_length=35, blank=False)
    last_name = models.CharField(verbose_name='Last Name', max_length=35, blank=False)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='Date Joined', default=timezone.now)
    last_location = models.PointField(verbose_name='Last Location', srid=4326, null=True, blank=True)

    # password field is already built-in
    # email and password are required by default

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['last_name', 'first_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        """ Does the user have a specific permission? """
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """ Does the user have permissions to view the app `app_label`? """
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """ Is the user a member of staff? """
        return self.staff

    @property
    def is_admin(self):
        """ Is the user an admin member? """
        return self.admin

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Convoy(models.Model):
    tracking = models.BooleanField(verbose_name='Tracking', default=False)
    updated = models.DateTimeField(verbose_name='Updated', auto_now=True)

    class Meta:
        verbose_name = 'Convoy'
        verbose_name_plural = 'Convoys'
        ordering = ['-tracking']

    def __str__(self):
        return str(self.id)


class Report(models.Model):
    CHOICES = (
        ('Yes', 'Yes, there are some civilians.'),
        ('No', 'No, there are no civilians.'),
        ('Unknown', 'I don\'t know'),
    )

    user = models.ForeignKey(User, verbose_name='User', editable=False, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(verbose_name='Image', upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    comment = models.TextField(verbose_name='Comment', blank=True)
    civilians = models.CharField(verbose_name='Civilians', choices=CHOICES, default='Unknown', max_length=35, blank=False)
    location = models.PointField(verbose_name='Location', srid=4326, null=True, blank=True)
    time = models.DateTimeField(verbose_name='Time', auto_now_add=True)
    verified = models.BooleanField(verbose_name='Verified', default=False)
    vehicles = models.CharField(verbose_name='Vehicles', max_length=35, blank=True)
    convoy = models.ForeignKey(Convoy, verbose_name='Convoy', on_delete=models.SET_NULL, null=True, blank=True)

    def latitude(self):
        return self.location.y

    def longitude(self):
        return self.location.x

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-verified']

    def __str__(self):
        return str(self.id)


class WorldBorder(models.Model):
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name
