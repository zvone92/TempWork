from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal

'''
class Job(models.Model):
    job_type = models.CharField(max_length=200)
    charging = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.job_type) + ": HRK" + str(self.charging)
'''


class Worker(models.Model):
    '''worker object is an ad that is going to be posted by user'''
    STATUS_CHOICES = {
        ('draft', 'Draft'),
        ('published', 'Published')
    }

    user     = models.ForeignKey(User, on_delete=models.CASCADE) #STVORITI OneToOne POLJE ZBOG UNIDIREKTOG ODNOSA
    name     = models.CharField(max_length=25, null=False)
    lastname = models.CharField(max_length=25, null=False)
    slug     = models.SlugField(max_length=120)
    dob      = models.DateField(null=True, blank=True)
    image    = models.ImageField(null=True, blank=True, upload_to='images', default='/images/default-avatar.png')
    cover    = models.ImageField(null=True, blank=True, upload_to='images', default='/images/default-avatar.png')
    skill    = models.CharField(max_length=25)
    details  = models.TextField(null=True, blank=True)
    phone    = PhoneNumberField(null=True, blank=True, unique=True)
    created  = models.DateTimeField(auto_now_add=True)
    medals   = models.ManyToManyField(User, related_name='medals', blank=True)
    status   = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    #def __str__(self):
    #    return  str(self.hourly_rate) + ": HRK"

    def summary(self):
        return self.details[:100]

    def total_medals(self):
        return self.medals.count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('worker_details', args=[self.id, self.slug])

    class Meta:
        verbose_name_plural = 'workers'


@receiver(pre_save, sender=Worker)
def pre_save_slug(sender, **kwargs):
    slug = slugify(kwargs['instance'].name)
    kwargs['instance'].slug = slug


class Profile(models.Model):
    '''Extended user model'''
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    dob     = models.DateField(null=True, blank=True)
    image   = models.ImageField(null=True, blank=True, upload_to='images', default='/images/default-avatar.png')

    def __str__(self):
        return self.user.username
