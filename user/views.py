from django.shortcuts import render,redirect
from . forms import RegisterForm,LoginForm

#10#
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid(): #Bunu çalıştırdığımzda forms.py'deki clean metodu çalışacak. Bilgiler eşleşiyorsa clean metodu username ve passwordu geri döndürüyordu. Şimdi o bilgileri almalıyız.
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        #Şimdi user modelinden bir tane obje oluşturup daha sonra bu objeyi kaydetmemiz gerekiyor.
        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()#Kullanıcı veri tabanına kaydedilmiş olacak.
            
        login(request,newUser)#Kayıt edilen kullanıcının giriş yapmış olmasını da istiyorsak:
        messages.success(request,"Başarıyla kayıt olundu.")
        return redirect("index") #Urls.py'deki path'te name olarak yazan kısmı buraya yazarsak o url'e gitmiş olacak.
    context = {
            "form":form
    }
    return render(request,"register.html",context)


def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid(): #Bu çalıştığında Django'nun kendisinde varsayılan olarak tanımlı Clean metodu çalışacak. Çünkü login için biz bir overrive yapmadık.Override yaptığımızda parola ile parola doğrula alanını ek olarak kontrol etmiştik.
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password) #Authenticate ile bilgiler eşleşiyor mu diye kontrol ediyoruz.
        if user is None: #Eğer herhangi bir bilgi gelmemişse
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı!")
            return render(request,"login.html",context)
        else: #Eğer bilgiler eşleşmişse
            messages.success(request,"Başarıyla giriş yapıldı.")
            login(request,user) #Kullanıcı girişini yapıyoruz.
            return redirect("index")
    else:#Form.is_valid kısmından bir eşleşme gelmezse login sayfasına tekrar geri dönecek.
        return render(request,"login.html",context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla çıkış yapıldı.")
    return redirect("index")