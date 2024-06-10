from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('saveuser/',views.saveuser,name='saveuser'),
    path('createurl/',views.createurl,name='createurl'),
     path('trackurl/<cipher>/',views.trackcipher,name='trackcipher'),
    path('trackurl/',views.trackurl,name='trackurl'),
    path('getviews/',views.getviews,name='getviews'), 
     path('myurl/<user_id>/',views.getMyUrls,name='myurls'),
    path('url/<short_url>/',views.displayurl,name='displayurl'),
    path('<short_url>/',views.displaysite,name='displaysite'),
    
]
