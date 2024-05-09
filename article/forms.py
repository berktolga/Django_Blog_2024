from django import forms
from . models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article #Formumuz ile modelimizi bağlantılı hale getiriyoruz.
        fields = ["title","content","article_image"] #Article-->Models.py'de olan ama sadece burada olmasını istediklerimiz yazıyoruz.
