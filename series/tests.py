from uuid import uuid4
from django.test import TestCase
from series.models import Episode, Serie
from django.contrib.auth.models import User

from rest_framework import status


# Create your tests here.

class TestSerie(TestCase):
    
    def _generate_user(self) -> User:
        return User.objects.create(username=f'fake username {uuid4()}', password='megaclave', email=f'fake email {uuid4()}')
    
    def _generate_serie(self):
        serie = Serie.objects.create(title=f'mock serie {uuid4()}', description=f'mock description')
        
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
        
    def test_create_serie(self):
        user = self._generate_user()
        self.client.force_login(user)
        
        serie_dict = {'title':f'mock serie {uuid4()}', 'description':f'mock description'}
        response = self.client.post(f'/api/series/', serie_dict)
        
        response_json = response.json()
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertIsInstance(response_json, dict)
        self.assertIsInstance(response_json.get('id'), int)
        self.assertIsInstance(response_json.get('title'), str)
        self.assertIsInstance(response_json.get('description'), str)