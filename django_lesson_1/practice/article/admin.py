from django.contrib import admin
from article.models import Article, Comments, CommentsOnComments

# Register your models here.

admin.site.register(Article)

class ComentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'article', 'created', 'moderation')


admin.site.register(Comments, ComentAdmin)

admin.site.register(CommentsOnComments)