from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import razorpay
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED
)

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from Ticketbookapi.form import user_signup_form,user_login_form
from .serializers import BookingSerializer, MovieSerializer
from .form import BookingModelForm, Payment_statusForm
from .models import Booking_models, Payment_status
from admin_show_site.models import Movie_details


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,)) 
def signup_user(request):
    signupform=user_signup_form(request.data)
    if signupform.is_valid():
        username=signupform.cleaned_data['username']
        email=signupform.cleaned_data['email']
        password=signupform.cleaned_data['password']
        conf_password=signupform.cleaned_data['conf_password']
        if password == conf_password:
            if User.objects.filter(username=username).exists():
                context={'signupform':signupform.data,'error':'username already exist'}
                return Response(context,status=HTTP_400_BAD_REQUEST)
            else:
                user=User.objects.create_user(username=username,
                                              email=email,
                                              password=password)                    
                user.save()
                context={'signupform':signupform.data,'success':'Created User'}
                return Response(context,status=HTTP_200_OK)
        else:
            context={'signupform':signupform.data,'error':'Password doesn\'t match'}
            return Response(context,status=HTTP_400_BAD_REQUEST)
    else:
        context={'signupform':signupform.errors,'error':'bad request'}
        return Response(context,status=HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login_user(request):
    loginform=user_login_form(request.data)
    if loginform.is_valid():
        username=loginform.cleaned_data['username']
        password=loginform.cleaned_data['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=HTTP_200_OK)
        else:
            return Response({"error": "Account is banned"}, status=HTTP_400_BAD_REQUEST)
    else:
        context={'loginform':loginform.errors,'Warning':'Enter a valid login credentials'}
        return Response(context, status=HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def moviedetails(request):
    movie_instance=Movie_details.objects.filter(is_active=True)
    serialize=MovieSerializer(movie_instance,many=True)
    return Response(serialize.data)

@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def movie_detail_view(request,uid):   
    try:
        data = Movie_details.objects.filter(is_active=True,id=uid)
        serialize = MovieSerializer(data,many=True)
        return Response(serialize.data)
    except Movie_details.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)    
    # data=get_object_or_404(Movie_details,id=uid)
    # serialize=MovieSerializer(data,many=True)
    # return Response(serialize.data)

@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logoutUser(request):
    logout(request)
    return Response("user logged out")


# razor payment methods

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))




@csrf_exempt
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def booking_model_view(request, movie_id):
    user = request.user
    form=BookingModelForm(request.data)
    if form.is_valid():
        seat = form.cleaned_data['seat']
        price = form.cleaned_data['price']
        count = form.cleaned_data['count']
        movie_details = Movie_details.objects.get(id=movie_id)
        total_price = price * count
        booking = Booking_models.objects.create(
                user_id=user,
                movie_id=movie_details,
                seat=seat,
                price=price,
                count=count,
                total_price=total_price
            )
        return Response({'success': 'Booking created'}, status=HTTP_200_OK)
    else:
        return Response({'error':'Invalid'}, status=HTTP_400_BAD_REQUEST)   
    


 
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))    
def new_order(request,uid):
    if request.method == "GET":
        
        data = Booking_models.objects.filter(movie_id=uid).order_by('-id').first()
        movie_ins=data.movie_id
        movie_name=movie_ins.name
        # movie_image=movie_ins.image
        movie_seat=data.seat
        movie_total=data.total_price

        # print("", request.POST['price'])
        # amount = int(request.POST['price'])
        # movie_name = Movie_details.objects.get(id=uid)

        new_order_response = razorpay_client.order.create({
                        "amount": movie_total*100,
                        "currency": "INR",
                        "payment_capture": "1"
                      })


        response_data = {
                "callback_url": "http://127.0.0.1:8000/Ticketbookapi/callback",
                "razorpay_key": "rzp_test_DCDK7quKT85NaG",
                "order": new_order_response,
                "name": movie_name,
                "seat": movie_seat,
        }
    

        # print(response_data)

        return JsonResponse(response_data)
    
    
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def order_callback(request):
    if request.method == "POST":
        paymentform = Payment_statusForm(request.data)
        if paymentform.is_valid():
           
            movie_id = request.data.get('movie_id') 
            customer_details = Booking_models.objects.filter(movie_id=movie_id).order_by('-id').first()
            order_id = paymentform.cleaned_data['order_id']
            payment_id = paymentform.cleaned_data['payment_id']
            payment_signature = paymentform.cleaned_data['payment_signature']
            print(customer_details)
            order_ins = Payment_status.objects.create(
                customer_details=customer_details,
                order_id=order_id,
                payment_id=payment_id,
                payment_signature=payment_signature,
              
            )
            order_ins.save()

            return JsonResponse({"res": "success"})
        else:
            return JsonResponse({"res": "Invalid data returned", "errors": paymentform.errors})
    else:
        return JsonResponse({"res": "Invalid request method"})

            
    



        
