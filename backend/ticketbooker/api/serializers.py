from rest_framework import serializers
from .models import *

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        
class TheatreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields = '__all__'

class ShowTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTiming
        fields = '__all__'
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'  # Or list all fields explicitly if needed
        

class ConfirmPaymentSerializer(serializers.Serializer):
    paymentIntentId = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    seats = serializers.ListField(child=serializers.CharField())
    userInfo = serializers.DictField()
    movieId = serializers.IntegerField()
    theatreId = serializers.IntegerField()
    showTimingsId = serializers.IntegerField()