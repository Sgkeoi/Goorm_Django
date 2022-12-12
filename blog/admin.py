from django.contrib import admin
from .models import Post, Category, Tag

admin.site.register(Post)
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    # 자동으로 slug 생성

# 태그 
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
# post와 Category를 가지고 오기    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)