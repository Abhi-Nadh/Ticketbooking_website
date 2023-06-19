from rest_framework import serializers
from admin_show_site.models import Movie_details
from .models import Booking_models



class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie_details
        fields= ('id','name','language','duration','genre','time','date','image','trailer')
    time = serializers.StringRelatedField()
    language = serializers.StringRelatedField(many=True)
    genre = serializers.StringRelatedField(many=True)


class BookingSerializer(serializers.ModelSerializer):
    # language = serializers.CharField(source='movie_id.language', read_only=True)
    duration = serializers.CharField(source='movie_id.duration', read_only=True)
    genre = serializers.StringRelatedField(many=True,source='movie_id.genre')
    time = serializers.CharField(source='movie_id.time', read_only=True)
    date = serializers.CharField(source='movie_id.date', read_only=True) 
    image = serializers.FileField(source='movie_id.image',read_only=True)   
    class Meta:
        model = Booking_models
        fields= ('id','user_id','movie_id','duration','language','genre','time'
                 ,'date','image','seat','price','count','total_price')
    user_id = serializers.StringRelatedField(many=False)
    movie_id = serializers.StringRelatedField(many=False)


    


   
