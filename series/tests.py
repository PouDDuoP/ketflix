from uuid import uuid4
from django.test import TestCase
from series.models import Episode, Serie

# Create your tests here.

class TestSerie(TestCase):
    
    def _generate_serie(self):
        serie = Serie.objects.create(title=f'mock serie {uuid4()}', description='mock description')
        
        for i in range(0, 6):
            Episode.objects.create(serie_id=serie.pk, name=f'mock episode {uuid4()}', number=i+1)
        
        return serie
    
    def test_retrieve_serie(self):
        serie = self._generate_serie()
        
        
        response = self.client.get(f'/api/series/{serie.pk}/')
        
        self.assertEqual(response.status_code, 200)
        
        response_json = response.json()
        
        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get('id'), int)
        self.assertIsInstance(response_json.get('title'), str)
        self.assertIsInstance(response_json.get('description'), str)
        self.assertIsInstance(response_json.get('episodes'), list)

        self.assertEqual(len(response_json.get('episodes')), 6)