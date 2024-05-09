from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

#1#
class Article(models.Model):#importtaki models'in içindeki Model class'ından türetmemiz gerekiyor.
    author = models.ForeignKey("auth.User", on_delete = models.CASCADE, verbose_name = "Yazar" )#Bu alanımız aslında user tablosuna işaret ediyor diyoruz. Yani buraya herhangi bir user yazdığımız zaman aslında o tablodaki user’ın direkt buraya geldiğini göreceğiz.
    title = models.CharField(max_length = 50,verbose_name = "Başlık")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True,verbose_name = "Oluşturulma Tarihi")
    article_image = models.FileField(blank = True, null = True,verbose_name="Makale Fotoğrafı")
    #4#
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["-created_date"] #En son eklenen makale ilk gösterilmesi için bunu ekledik.

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete = models.CASCADE,verbose_name="Makale",related_name = "comments")
    #Her bir article'ın birçok comment'i olabilir. ForeignKey yardımıyla comment'leri article'lara bağlayacağız.
    #Makale silindiğinde yorumların da silinmesi için "on_delete" kullandık.
    #Article'ların comment'lerine ulaşabilmel için "related_name" kullandık.(Articles.comments diyerek comments tablosuna da erişebileceğiz.)
    comment_author = models.CharField(max_length = 50, verbose_name = "İsim")
    comment_content = models.CharField(max_length = 200, verbose_name ="Yorum")
    comment_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):#Comment'i özelleştirebiliriz. Yorumun içeriğini admin panelindeki kısımda göstermek için:
        return self.comment_content

    class Meta:
        ordering = ["-comment_date"] #En son eklenen yorum ilk gösterilmesi için bunu ekledik.