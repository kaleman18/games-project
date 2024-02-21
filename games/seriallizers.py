from rest_framework import serializers
from .models import Game

class GamesSerializer(serializers.ModelSerializer):

    class Meta:
        
        #needs two things fields and a model

        fields = ('id','owner','name','description','created_at')
        model = Game
