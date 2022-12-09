from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    # 자동으로 slug 생성

# post와 Category를 가지고 오기    
admin.site.register(Category, CategoryAdmin)