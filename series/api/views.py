from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from series.api.serializers import SerieSerializer

from series.models import Serie


# class SerieApiView(APIView):
# class SerieApiView(viewsets.ViewSet):
class SerieApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = Serie.objects.all()
    serializer_class = SerieSerializer
    
    def list(self, request):
        series = SerieSerializer(Serie.objects.all(), many=True)
        return Response(data=series.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk: int):
        series = SerieSerializer(Serie.objects.get(pk=pk))
        return Response(data=series.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serie = SerieSerializer(data=request.POST)
        serie.is_valid(raise_exception=True)
        Serie.objects.create(title=serie.validated_data['title'], description=serie.validated_data['description'])
        return self.list(request)