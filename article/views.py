from django.shortcuts import render, HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm
from django.contrib import messages
from . models import Article,Comment #Article ve Comment modellerini dahil etmiş oluyoruz.(Model.py'den)
from django.contrib.auth.decorators import login_required

# Create your views here.

#6#
def index(request):
    context = {
        "numbers":[1,2,3,4,5]
    }
    return render(request,"index.html",context)
    #return HttpResponse("Anasayfa")

def experiments(request):
    return render(request,"experiments.html")

def detail(request,id):
    #id'sine göre bir makale gelecek ve bu obje liste içerisinde dönecek.
    #article = Article.objects.filter(id = id).first() #Obje liste içerisinde geldiği için first metodunu kullandık. Listede zaten id'ye göre bir makale gelmiş olacak ve onu listeden çekmiş olacağız.
    article = get_object_or_404(Article, id = id)
    comments = article.comments.all() #Article'ın ilişkili olduğu yorumların hepsini aldık.
    return render(request,"detail.html",{"article":article,"comments":comments}) 

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    incoming_article_context = { #Dashboard kısmına sözlük yapısı ile gönderim yapacağız.
        "articles": articles #Key-value
    }
    return render(request,"dashboard.html",incoming_article_context)

@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False) #Save metoduna diyoruz ki commit yani save işlemini sen yapma. Bunu daha sonra biz yapacağız.
        article.author = request.user #Article'ın yazarına şu anki giriş yapan kullanıcıyı atıyoruz.
        article.save() #Son olarak article'ı biz save ediyoruz.
        messages.success(request,"Makale başarıyla oluşturuldu.")
        return redirect("article:dashboard")
    #Article-->Forms.py'de Model Form olarak oluşturduğumuz ArticleForm'dan bir obje oluşturmalıyız.
    form = ArticleForm()
    article_context = {
        "form":form
    }
    return render(request,"addArticle.html",article_context)

@login_required(login_url="user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None,request.FILES or None, instance = article) #instance sayesinde düzenleme formunda makale içereği hazır halde karşımıza gelecek.
    if form.is_valid():
        article = form.save(commit=False) #Save metoduna diyoruz ki commit yani save işlemini sen yapma. Bunu daha sonra biz yapacağız.
        article.author = request.user #Article'ın yazarına şu anki giriş yapan kullanıcıyı atıyoruz.
        article.save() #Son olarak article'ı biz save ediyoruz.
        messages.success(request,"Makale başarıyla güncellendi.")
        return redirect("article:dashboard")
    return render(request,"update.html",{"form":form})

@login_required(login_url="user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id=id)
    article.delete()
    messages.success(request,"Makale başarıyla silindi.")
    return redirect("article:dashboard") #Article uygulaması(klasöründeki) url dosyasından dashboard'a gidicek.

def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains = keyword) # İçinde keywordun geçtiği makaleleri döndürecek.
        return render(request,"articles.html",{"articles":articles})
    articles = Article.objects.all()
    return render(request,"articles.html",{"articles":articles})

def addComment(request,id):
    #id'ye göre post'u almamız gerekiyor. 
    article = get_object_or_404(Article,id=id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author=comment_author,comment_content=comment_content)
        newComment.article = article
        newComment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))