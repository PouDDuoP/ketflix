from django.test import TestCase


class TestSerie(TestCase):
    def test_retrieve_serie(self):
        response = self.client.get(f'/api/series/')
        
        self.assertEqual(response.status_code, 200)