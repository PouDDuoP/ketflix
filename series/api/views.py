import logging
from rest_framework import status, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from series.api.permissions import IsMeOrReadOnly

from series.api.serializers import DetailEpisodeSerializer, EpisodeSerializer, ScoreEpisodeSerializer, SerieSerializer, DetailSeriesSerializer, ScoreSerializer

from series.models import Episode, Serie


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

class SerieApiView(ModelViewSet):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsMeOrReadOnly]
    serializer_class = SerieSerializer
    queryset = Serie.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailSeriesSerializer  
        if self.action == 'set_score':
            return ScoreSerializer
        else:
            return self.serializer_class
        
    @action(detail=True, methods=['PUT'], url_path='set-score', permission_classes=[IsAdminUser])
    def set_score(self, request, pk: int):
        data = {'serie': pk, 'user': request.user.pk, 'score': int(request.data.get('score'))}

        serializer = self.get_serializer_class()(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(status=status.HTTP_200_OK)
    

class EpisodesApiView(ModelViewSet):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsMeOrReadOnly]
    serializer_class = EpisodeSerializer
    queryset = Episode.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailEpisodeSerializer  
        if self.action == 'set_score':
            return ScoreEpisodeSerializer
        else:
            return self.serializer_class
        
    @action(detail=True, methods=['PUT'], url_path='set-score', permission_classes=[IsAdminUser])
    def set_score(self, request, pk: int):
        data = {'episode': pk, 'user': request.user.pk, 'score': int(request.data.get('score'))}

        serializer = self.get_serializer_class()(data=data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(status=status.HTTP_200_OK)