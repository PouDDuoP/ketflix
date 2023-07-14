from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from series.api.serializers import SerieSerializer, DetailSeriesSerializer

from series.models import Serie


# class SerieApiView(APIView):
# class SerieApiView(viewsets.ViewSet):
# class SerieApiView(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
    
#     queryset = Serie.objects.all()
#     serializer_class = SerieSerializer
    
#     def list(self, request):
#         series = SerieSerializer(Serie.objects.all(), many=True)
#         return Response(data=series.data, status=status.HTTP_200_OK)
    
#     def retrieve(self, request, pk: int):
#         series = SerieSerializer(Serie.objects.get(pk=pk))
#         return Response(data=series.data, status=status.HTTP_200_OK)
    
#     def create(self, request):
#         serie_serializer = SerieSerializer(data=request.POST)
#         serie_serializer.is_valid(raise_exception=True)
        
#         serie_serializer.save()
#         return self.list(request)

    # def update(self, request):
    #     serie_serializer = SerieSerializer(data=request.POST)
    #     serie_serializer.is_valid(raise_exception=True)
        
    #     serie_serializer.save()
    #     return self.list(request)

class SerieApiView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SerieSerializer
    queryset = Serie.objects.all()
    
    def get_serializer_class(self):
        serializer = self.serializer_class
        
        if self.action == 'retrieve':
            serializer = DetailSeriesSerializer  
        
        return serializer