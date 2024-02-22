from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Game
from .seriallizers import GamesSerializer
from .permissions import IsOwnerOrReadOnly


class GameList(ListCreateAPIView):

    queryset = Game.objects.all()


    #serializing
    serializer_class = GamesSerializer


class GameDetail(RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GamesSerializer
    permission_classes = (IsOwnerOrReadOnly,)

