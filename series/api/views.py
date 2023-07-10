from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from series.models import Serie


class SerieApiView(APIView):
    def get(self, request):
        series = [serie.title for serie in Serie.objects.all()]
        return Response(data=series, status=status.HTTP_200_OK)
    
    def post(self, request):
        Serie.objects.create(title=request.POST['title'], description=request.POST['description'])
        return self.get(request)