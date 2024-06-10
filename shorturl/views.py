import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
import random
from django.shortcuts import redirect

def home(request):
    # if request.method=='POST':
    #     plainUrl=request.POST['plainurl']
    #     cipherUrl=generateShortUrl()
    #     storeUrl(cipherUrl,plainUrl)
    return render(request,'home.html')

def login(request):
    return render(request,'login.html')

def register(request):
    if request.method=='POST':
        email=request.POST['email']
        user=Userdetail.objects.filter(email=email)
        if len(user)==0:
            ob=Userdetail()
            ob.username=request.POST['name']
            ob.email=email
            password=request.POST['password']
            ob.password=make_password(password)
            ob.save()
            return render(request,'login.html')
    return render(request,'register.html')

@csrf_exempt 
def saveuser(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            email=data['email']
            password=data['password']
            user=Userdetail.objects.filter(email=email)
            if len(user)==0:
                return JsonResponse({'user_id':0})
            isValidPassword=check_password(password,user[0].password)
            if isValidPassword:
                return JsonResponse({'user_id':int(user[0].user_id)})
        except Exception as e:
            print(e)
            return JsonResponse({'user_id':0})
    return JsonResponse({'user_id':0})

def displayurl(request,short_url):
    full_url = request.build_absolute_uri('/') 
    dict_data={'shorturl':full_url+short_url}
    dict_data['cipherurl']=short_url
    myOb=Url.objects.filter(cipher_url=short_url)
    if len(myOb)>0:
        dict_data['originalUrl']=myOb[0].plain_url
    return render(request,'home.html',dict_data)

def displaysite(request,short_url):
    url_ob=Url.objects.filter(cipher_url=short_url)
    if len(url_ob)>0:
        url_ob[0].views=int(url_ob[0].views)+1
        url_ob[0].save()
        print(url_ob[0].plain_url) 
        return render(request,'redirectUrl.html',{'redirecturl':url_ob[0].plain_url})
    return redirect('home')

def getMyUrls(request,user_id):
    if user_id:
        myOb=Url.objects.filter(url_user_id=user_id)
        if len(myOb)>0:
            return render(request,'myurls.html',{'myUrl':myOb})
    return render(request,'myurls.html')

def trackurl(request):
    return render(request,'trackurl.html',{'cipherurl':""})
@csrf_exempt 
def createurl(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            url=data['plainurl']
            user_ID=data['user_ID']
            if url.startswith("https://")==False:
                url="https://"+url
            cipherurl=storeUrl(url,user_ID)
            full_url = request.build_absolute_uri('/')
            return JsonResponse({'shorturl':full_url+"url/"+cipherurl,'plainurl':url})
        except Exception as e:
            print(e)
            return JsonResponse({'shorturl':""})
    return JsonResponse({'shorturl':""})

@csrf_exempt 
def getviews(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            url=str(data['shorturl'])
            cipherUrl=None
            if len(url)==5:
                cipherUrl=url 
            else:               
                cipherUrl=url[url.rindex('/')+1:]
            print(cipherUrl)
            url_ob=Url.objects.filter(cipher_url=cipherUrl)
            if len(url_ob)>0:
                views=int(url_ob[0].views) 
                return JsonResponse({'views':views})    
            return JsonResponse({'views':0})
        except Exception as e:
            print(e)
            return JsonResponse({'views':0})
    return JsonResponse({'views':0})


def storeUrl(plainUrl,user_id):
    cipherurl=generateShortUrl()
    ob=Url()
    ob.plain_url=plainUrl
    ob.cipher_url=cipherurl
    if user_id!=0:
        user_ob=Userdetail.objects.get(user_id=user_id)
        ob.url_user_id=user_ob
    ob.views=0
    ob.save()
    print(cipherurl,plainUrl,user_id)
    return cipherurl
def trackcipher(request,cipher):
    full_url = request.build_absolute_uri('/')+cipher

    url_ob=Url.objects.filter(cipher_url=cipher)
    views=0
    if len(url_ob)>0:
        views=int(url_ob[0].views)
        return render(request,'trackurl.html',{'cipherurl':full_url,'views':views})
    return render(request,'trackurl.html',{'cipherurl':full_url})
def generateShortUrl():
    characters='abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789'
    randomUrl=''.join(random.sample(characters,5))
    return randomUrl
