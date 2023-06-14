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
    class Meta:
        model = Booking_models
        fields= ('id','user_id','movie_id','seat','price','count','total_price')
    user_id = serializers.StringRelatedField(many=False)
    movie_id = serializers.StringRelatedField(many=False)


    


   
