
from typing import Dict
from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from series.models import Episode, ScoreEpisode, Serie, Score
from django.db.models.aggregates import Avg


# class SerieSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=True)
    # description = serializers.CharField(required=True)
    
    # def validate(self, serie: Dict[str, str]):
    #     if not serie.get('title'):
    #         raise ValidationError('Title is mandatory')
    #     return serie
    
    # def validate_title(self, title: str):
    #     series = Serie.objects.filter(title=title)
    #     if series.exists():
    #         raise ValidationError('The title already exists')
    #     return title
    
    # def validate_description(self, description: str):
    #     if not description:
    #         raise ValidationError('The description cannot ne blank')
    #     return description
    
    # def create(self, **kwargs) -> Serie:
    #     serie = Serie.objects.create(**self.validated_data)
    #     return serie
    
    # def update(self, **kwargs) -> Serie:
    #     for attr, value in self._validated_data.items():
    #         setattr(self.instance, attr, value)
            
    #     self.instance.save()
    #     return self.instance()
    
    # def save(self, **kwargs):
    #     if not self.instace:
    #         self.instance = self.create()
    #     elif self.instance:
    #         self.instance = self.update()
            
    #     return self.instance


class SerieSerializer(ModelSerializer):
    
    class Meta:
        model = Serie
        fields = ('id', 'title', 'description')
        
class EpisodeSerializer(ModelSerializer):

    class Meta:
        model = Episode
        fields = ('id', 'name')
        
class DetailSeriesSerializer(ModelSerializer):
    episodes = EpisodeSerializer(source='episode_set', many=True)
    score = SerializerMethodField()
    
    def get_score(self, serie: Serie) -> int:
        return Score.objects.filter(serie=serie.pk).aggregate(score=Avg(('score'))).get('score')
    
    class Meta:
        model = Serie
        fields = ('id', 'title', 'description', 'episodes','score')
        
class DetailEpisodeSerializer(ModelSerializer):
    score = SerializerMethodField()
    
    def get_score(self, serie: Episode) -> int:
        return ScoreEpisode.objects.filter(episode=Episode.pk).aggregate(score=Avg(('score'))).get('score')
    
    class Meta:
        model = Episode
        fields = ('id', 'name', 'score')

class ScoreSerializer(ModelSerializer):

    class Meta:
        model = Score
        fields = ('id', 'user', 'serie', 'score')

class ScoreEpisodeSerializer(ModelSerializer):

    class Meta:
        model = ScoreEpisode
        fields = ('id', 'user', 'episode', 'score')