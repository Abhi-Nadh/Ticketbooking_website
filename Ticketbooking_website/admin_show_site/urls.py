from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        path('',views.admin_home.as_view(),name='home'),
        path('login',views.admin_login,name='login'),
        path('addmovies',views.add_movies,name='addmovie'),
        path('logout',views.logout_user,name='logout'),
        path('editmovies/<int:uid>',views.editfilm,name='editmovies'),
        path('detail/<int:uid>',views.detailview,name='details'),
        path('deletemovies/<int:uid>',views.deletfilm,name='deletemovies'),
        path('changestatus',views.changestatus,name='changestatus'),
        path('search',views.search_m,name='search'),
        path('manageuser',views.user_manage,name='manageuser'),
        path('changeuserstatus',views.changeuserstatus,name='changeuserstatus'),
                ]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 