from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
from django.contrib.admin.decorators import register

from series.models import Serie, Episode

class SeriesAdmin(ModelAdmin):
    pass
    
admin.site.register(Serie, SeriesAdmin)

@register(Episode)
class EpisodesAdmin(ModelAdmin):
    pass
    