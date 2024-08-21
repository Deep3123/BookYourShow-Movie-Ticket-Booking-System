from django.shortcuts import render
from rest_framework import viewsets 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import * 
from api.models import *
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.conf import settings
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.utils import timezone


class MovieView(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()  

@api_view(['GET'])
def theatre_list(request):
    movie_id = request.GET.get('movieId')
    if movie_id:
        theatres = Theatre.objects.filter(movies__id=movie_id)
    else:
        theatres = Theatre.objects.all()
    serializer = TheatreSerializer(theatres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def show_timings_list(request):
    theatre_id = request.GET.get('theatreId')
    movie_id = request.GET.get('movieId')
    if theatre_id and movie_id:
        show_timings = ShowTiming.objects.filter(theatre_id=theatre_id, movie_id=movie_id)
    else:
        show_timings = ShowTiming.objects.all()
    serializer = ShowTimingSerializer(show_timings, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email') 
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, email=email, password=password)  # Include email when creating user
    refresh = RefreshToken.for_user(user)
    
    return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return (
            six.text_type(user.pk) + user.password + six.text_type(timestamp) + six.text_type(login_timestamp)
        )
    
    def _check_token(self, user, token, timestamp):
        expiration_time = timezone.now() - timezone.timedelta(hours=1)
        if expiration_time.replace(microsecond=0, tzinfo=None) > timestamp:
            return False
        return super()._check_token(user, token, timestamp)

custom_token_generator = CustomPasswordResetTokenGenerator()


class CustomPasswordResetAPI(APIView):
    def post(self, request):
        email = request.data.get('email', None)
        
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        UserModel = get_user_model()
               
        active_users = UserModel._default_manager.filter(email__iexact=email, is_active=True)
        
        for user in active_users:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = custom_token_generator.make_token(user)
            reset_link = f"http://localhost:3000/reset-password/{uid}/{token}"
            mail_subject = 'Reset your password for BookYourShow'
            message = f"Click the link below to reset your password:\n{reset_link}"
            
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])
        return Response({'success': 'An email with password reset instructions has been sent.'}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPI(APIView):
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')
        
        if not uid or not token or not password:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
        
        UserModel = get_user_model()
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = UserModel.objects.get(pk=uid)
            
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        
        if user is not None and custom_token_generator.check_token(user, token):
            user.set_password(password)
            user.save()
            return Response({'success': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token is invalid or has expired'}, status=status.HTTP_400_BAD_REQUEST)


stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
@csrf_exempt
def create_payment_intent(request):
    try:
        data = json.loads(request.body)
        amount = data['amount']
        payment_method_id = data.get('paymentMethodId')
        
        if not payment_method_id:
            return JsonResponse({'error': 'Missing payment method ID'}, status=400)
        
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='inr',
            payment_method_types=['card'],
            payment_method=payment_method_id,
        )
        return JsonResponse({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)
