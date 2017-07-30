from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _


class Program(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    desc = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=1,
                                choices=(
                                    ('E', _('English')), ('K', _('Korean')),
                                ), default='E')

    def __str__(self):
        return self.name + ' ' + _('Program')

    def get_absolute_url(self):
        return reverse('program_generic:update', kwargs={'pk': self.pk})


class Url(models.Model):
    program = models.ForeignKey(Program, null=True, blank=True)
    category = models.CharField(max_length=1,
                                choices=(
                                    ('S', _('Slide')), ('P', _('PDF')), ('V', _('Video')),)
                                )
    location = models.CharField(max_length=255)
    ORDER = models.IntegerField(default=0, null=True)

    class Meta:
        ordering = ('ORDER', )

