from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View

from series.models import Serie, Episode

# Create your views here.
class SerieView(View):

    def get(self, request): 
        context = {
            'series' : list(Serie.objects.all())
        }
        
        return render(request, 'series.html', context=context)
    
class EpisodeView(View):

    def get(self, request, serie_id: int): 
        context = {
            'episodes' : list(Episode.objects.filter(serie_id=serie_id))
        }
        
        return render(request, 'episodes.html', context=context)