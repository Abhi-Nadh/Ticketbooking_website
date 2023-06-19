from tkinter import Canvas
from django.conf import settings
from django.http import HttpResponse, JsonResponse
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
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
import qrcode




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
        language = form.cleaned_data['language']
        price = form.cleaned_data['price']
        count = form.cleaned_data['count']
        movie_details = Movie_details.objects.get(id=movie_id)
        total_price = price * count
        booking = Booking_models.objects.create(
                user_id=user,
                movie_id=movie_details,
                seat=seat,
                language=language,
                price=price,
                count=count,
                total_price=total_price
            )
        data = Booking_models.objects.filter(movie_id=movie_id).order_by('-id').first()
        data_id=data.id
        # return Response({'success': 'Booking created'}, status=HTTP_200_OK)
        return Response(data_id)
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
        data_id=data.id

        # print("", request.POST['price'])
        # amount = int(request.POST['price'])
        # movie_name = Movie_details.objects.get(id=uid)

        new_order_response = razorpay_client.order.create({
                        "amount": movie_total*100,
                        "currency": "INR",
                        "payment_capture": "1"
                      })


        response_data = {
                "razorpay_key": "rzp_test_DCDK7quKT85NaG",
                "order": new_order_response,
                "name": movie_name,
                "seat": movie_seat,
                "data_id": data_id
        }
    

        # print(response_data)

        return JsonResponse(response_data)
    
    
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def order_callback(request):
    if request.method == "POST":
        paymentform = Payment_statusForm(request.data)
        print(paymentform)
        # if paymentform.is_valid():
        customer_details = paymentform.cleaned_data['customer_details']
        # customer_details = payment_status.customer_details
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
        # else:
        #     return JsonResponse({"res": "Invalid data returned", "errors": paymentform.errors})
    else:
        return JsonResponse({"res": "Invalid request method"})


@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))   
def display_booking_model_data(request,uid):
    model_data=Booking_models.objects.get(id=uid)
    serialize=BookingSerializer(model_data)

    return JsonResponse(serialize.data)
    
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))   
def get_user_booked_movies(request):
    user = request.user.id
    movies = Booking_models.objects.filter(user_id_id=user).order_by('-id') 
    if movies:   
        serializer = BookingSerializer(movies,many=True)
        return Response(serializer.data)
    else:
        return JsonResponse({"error":"nothing"})
    
    
    
# from reportlab.pdfgen import canvas  
# from reportlab.lib import colors
# from django.http import HttpResponse

# @csrf_exempt
# @api_view(['GET'])
# @permission_classes((IsAuthenticated,))
# def ticket_pdf(request):
#     pdf_model = Payment_status.objects.last() 
#     movie_name = pdf_model.customer_details.movie_id.name
#     language = pdf_model.customer_details.movie_id.language
#     genre = pdf_model.customer_details.movie_id.genre
#     date =  pdf_model.customer_details.movie_id.date
#     time =  pdf_model.customer_details.movie_id.time
#     seat =  pdf_model.customer_details.seat
#     price = pdf_model.customer_details.total_price
#     orderid = pdf_model.order_id

#     response = HttpResponse(content_type="application/pdf")
#     # response["Content-Disposition"] = 'attachment; filename="movie_ticket.pdf"'
#     response.headers = {   
#             'Content-Type': 'application/pdf',
#             'Content-Disposition': 'attachment;filename="movie_ticket.pdf"',
#         }
#     pagesize = ((700, 350))

#     p = canvas.Canvas(response, pagesize=pagesize)
  
#     p.setFont("Helvetica", 20)
#     p.drawString(50, 270, f"Movie: {movie_name}")
#     p.drawString(50, 260, f"Language: {language}")
#     p.drawString(50, 250, f"Genre: {genre}")
#     p.drawString(50, 240, f"Date: {date}")
#     p.drawString(50, 210, f"Time: {time}")
#     p.drawString(50, 180, f"Seat: {seat}")
#     p.drawString(50, 150, f"Price: Rs-{price}")
#     p.drawString(50, 120, f"OrderID: {orderid}")

#     styles = getSampleStyleSheet()
#     title_style = styles["Heading1"]
#     title_style.textColor = colors.red
#     title_style.fontName = "Helvetica-Bold"
#     title_style.alignment = 1 
#     title_style.fontSize = 40

#     # Draw the "Movie Ticket" text with the custom style
#     p.setFont(title_style.fontName, title_style.fontSize)
#     p.setFillColor(title_style.textColor)
#     p.drawCentredString(350, 300, "Movie Ticket")
   
#     # Save the PDF
#     p.showPage()
#     p.save()

#     return response




@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def ticket_pdf(request):
    pdf_model = Payment_status.objects.last() 
    movie_name = pdf_model.customer_details.movie_id.name
    # language = pdf_model.customer_details.movie_id.language
    # genre = pdf_model.customer_details.movie_id.genre
    count = pdf_model.customer_details.count
    date = pdf_model.customer_details.movie_id.date
    time = pdf_model.customer_details.movie_id.time
    seat = pdf_model.customer_details.seat
    price = pdf_model.customer_details.total_price
    orderid = pdf_model.order_id
    payment_id = pdf_model.payment_id
    payment_signature = pdf_model.payment_signature
    
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="movie_ticket.pdf"'
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=((700,400)))
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.textColor = colors.red
    title_style.fontName = "Helvetica-Bold"
    title_style.alignment = 1 
    title_style.fontSize = 40
    
    elements.append(Spacer(1, 1))
    
    
    # Add "Movie Ticket" title
    title_text = Paragraph("Movie Ticket", title_style)
    elements.append(title_text)
    spacer = Spacer(1, 50)
    elements.append(spacer)

    # Add movie details
    movie_details = [
        f"Movie: {movie_name}",
        # f"Language: {language}",
        # f"Genre: {genre}",
        f"Date: {date} ",
        f"Time: {time} ",
        f"Seat: {seat} ",
        f"Price: Rs-{price} ",
        f"OrderID: {orderid} ",
        f"Payment ID: {payment_id} ",
        f"Payment Signature: {payment_signature}",
    ]
    
    data_qr=f"Movie: {movie_name}\nDate: {date}\nTime: {time}\nSeat: {seat}\ncount: {count}price: {price}"

    
    for detail in movie_details:
        detail_text = Paragraph(detail, styles["Normal"])
        elements.append(detail_text)
    
    # Generate QR code containing all the data
    qr_code_data = data_qr
    print(qr_code_data)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_code_data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Resize the QR code image
    max_image_width = 400
    max_image_height = 60  # Adjust the height as per your requirement
    qr_image.thumbnail((max_image_width, max_image_height))
    
    # Add QR code to PDF as an Image object
    qr_image_io = io.BytesIO()
    qr_image.save(qr_image_io, format='PNG')
    qr_image_io.seek(0)
    qr_image_obj = Image(qr_image_io, width=qr_image.width, height=qr_image.height)
    elements.append(qr_image_obj)
    
    doc.build(elements)
    
    pdf_data = buffer.getvalue()
    buffer.close()
    
    response.write(pdf_data)
    response = HttpResponse(pdf_data, content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="movie_ticket.pdf"'
    
    return response

