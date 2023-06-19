from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        path('signup',views.signup_user,name='signupapi'),
        path('login',views.login_user,name='loginapi'),
        path('movielist',views.moviedetails,name='movielistapi'),
        path('logout',views.logoutUser,name='logoutapi'),
        path('moviedetails/<int:uid>',views.movie_detail_view,name='detailapi'),
        path('bookingmovie/<int:movie_id>',views.booking_model_view,name='bookingmovie'),
        # path('finalconfirm/<int:uid>',views.final_confirm,name='bookingmovie'),
        path('neworder/<int:uid>',views.new_order,name='neworder'),
        path('callback',views.order_callback,name='callback'),
        path('display_model/<int:uid>',views.display_booking_model_data,name='display_model'),
        path('usermovies',views.get_user_booked_movies,name='usermovies'),
        path('ticket',views.ticket_pdf,name='ticket'),
                ]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 
