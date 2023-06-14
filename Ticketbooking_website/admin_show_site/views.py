from datetime import datetime
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView
from admin_show_site.form import Add_Movie_Form, LoginForm
from admin_show_site.models import Movie_details
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt



def check_superuser(user):
    return user.is_superuser


def admin_login(request):
    # loginform=LoginForm()
    if request.method=='POST':
        loginform=LoginForm(request.POST)
        if loginform.is_valid():
            email=loginform.cleaned_data['email']
            password=loginform.cleaned_data['password']
            if User.objects.filter(email=email).exists():
                username = User.objects.get(email=email).username
                user=authenticate(request,username=username,password=password)

                if user is not None:
                    login(request,user)
                    return redirect('home')
                else:
                    messages.error(request,'Incorrect password')
                    return redirect('login')
            else:
                messages.error(request,'Incorrect Email id')  
                return redirect('login') 
        else:
            messages.error(request,'Corrupted Inputs')  
            return redirect('login')
    else:
        loginform=LoginForm()
        return render(request,'admin_login.html',{"loginform":loginform}) 

                               
  
# @user_passes_test(check_superuser,login_url = reverse_lazy('login'))
class admin_home(UserPassesTestMixin,ListView):
    model = Movie_details
    template_name = "admin_home.html"
    context_object_name='movielist'
    paginate_by=8
    def test_func(self):
        return self.request.user.is_superuser
    def get_login_url(self):
        return 'login'

def search_m(request):
    search=request.GET['search']
    fdate = request.GET.get('fdate')
    ldate = request.GET.get('ldate')
    movie = Movie_details.objects.filter(name__icontains=search) 
    if fdate and ldate:
        try:
            fdate = datetime.fromisoformat(fdate).date()
            ldate = datetime.fromisoformat(ldate).date()
            movie = movie.filter(date__range=[fdate, ldate])
        except ValueError:
            pass

    return render(request, 'search.html', {'movie': movie})   
    
    
    
@user_passes_test(check_superuser,login_url = reverse_lazy('login'))   
def add_movies(request):
    if request.method == 'POST':
        addform = Add_Movie_Form(request.POST, request.FILES)
        if addform.is_valid():
            movie = addform.save(commit=False)
            movie.save()
            addform.save_m2m()
            print(movie)
            # movie=addform.save()
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, "Invalid data")
            addform = Add_Movie_Form()
            return render(request, "admin_addmovies.html",{'addform':addform})
    else:
        addform = Add_Movie_Form()
    return render(request, "admin_addmovies.html", {'addform': addform})

@user_passes_test(check_superuser,login_url = reverse_lazy('login'))   
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

@user_passes_test(check_superuser,login_url=reverse_lazy('login'))
def editfilm(request,uid):
    data=get_object_or_404(Movie_details,id=uid)
    updateform=Add_Movie_Form(instance=data)
    if request.method=='POST':
        updateform=Add_Movie_Form(request.POST,request.FILES,instance=data)
        if updateform.is_valid():
            editmovie=updateform.save(commit=False)
            editmovie.save()
            updateform.save_m2m()
            return redirect('home')
        else:
            return HttpResponseRedirect(reverse('home'))
    else:
        return render(request,'admin_editmovie.html',{'editdata':updateform})
    
@user_passes_test(check_superuser,login_url=reverse_lazy('login'))
def detailview(request,uid):
    data=get_object_or_404(Movie_details,id=uid)
    return render(request,'detailview.html',{'data':data})
    
    
def deletfilm(request,uid):
    data=get_object_or_404(Movie_details,id=uid)
    data.delete()
    return redirect('home')



@csrf_exempt
@user_passes_test(check_superuser,login_url = reverse_lazy('login'))
def changestatus(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        movie_id = int(request.POST['movie'])
        action = request.POST['action']
        movie_instance = Movie_details.objects.get(id=movie_id)
        if action == "disable":
            movie_instance.is_active = 0
        else:
            movie_instance.is_active = 1
        movie_instance.save()
        return JsonResponse({'result':'success'})
 

@csrf_exempt
@user_passes_test(check_superuser,login_url = reverse_lazy('login'))
def changeuserstatus(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_id = int(request.POST['user'])
        action = request.POST['action']
        user_instance = User.objects.get(id=user_id)
        if action == "disable":
            user_instance.is_active = 0
        else:
            user_instance.is_active = 1
        user_instance.save()
        return JsonResponse({'result':'success'})
   

@user_passes_test(check_superuser,login_url=reverse_lazy('login'))
def user_manage(request):
    user_data=User.objects.all()
    return render(request,'usermanage.html',{'data':user_data})
    

    


