from django.contrib import admin
from . import models

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title','content','pub_time')
admin.site.register(models.Article,ArticleAdmin)
