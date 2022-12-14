from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Category, Tag, Comment

# ---------------------------------------------------------------------------

admin.site.register(Post, MarkdownxModelAdmin)
# Register your models here.

admin.site.register(Comment)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    # 자동으로 slug 생성

# 태그 
class TagAdmin(admin.ModelAdmin) :
    prepopulated_fields = {'slug' : ('name', )}
    
# post와 Category를 가지고 오기    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)