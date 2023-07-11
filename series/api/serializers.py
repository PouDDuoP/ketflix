
from typing import Dict
from django.forms import ValidationError
from rest_framework import serializers
from series.models import Serie


class SerieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    def validate(self, serie: Dict[str, str]):
        if not serie.get('title'):
            raise ValidationError('Title is mandatory')
        return serie
    
    class Meta:
        model = Serie
        fields = '__all__'