from django.db import models

class Userdetail(models.Model):
    user_id=models.BigAutoField(primary_key=True)
    username=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
class Url(models.Model):
    url_id=models.BigAutoField(primary_key=True)
    url_user_id=models.ForeignKey(Userdetail,on_delete=models.SET_NULL,null=True,blank=True)
    cipher_url=models.CharField(max_length=8)
    plain_url=models.CharField(max_length=5000)
    views=models.IntegerField(default=0)
