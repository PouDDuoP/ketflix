from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin

from series.models import Serie, Episode

# Create your views here.
class SerieView(View):

    def get(self, request): 
        if request.user.is_authenticated:
            context = {
                'series' : list(Serie.objects.all())
            }
        
            return render(request, 'series.html', context=context)
        return redirect('login')
        
class EpisodeView(LoginRequiredMixin, View):

    def get(self, request, serie_id: int): 
        context = {
            'episodes' : list(Episode.objects.filter(serie_id=serie_id))
        }
        
        return render(request, 'episodes.html', context=context)