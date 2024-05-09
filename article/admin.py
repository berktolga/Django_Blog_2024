from django.contrib import admin

from .models import Article,Comment
# Register your models here.

#2#
#2.1#
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title","author","created_date"]
    search_fields = ["title"]
    list_filter = ["created_date"]
    class Meta:
        model = Article

admin.site.register(Comment)