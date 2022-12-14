from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
import os

# DB 연동
# 1. 함수를 사용하는 방법
# 2. Class를 사용하는 방법

# 클래스로 지정하기 때문에 내어쓰기 합니다.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # max_length=50 : 제목 50자, unique=True : 유일값 출력(똑같은 제목은 넣을 수 없습니다.)
    # post는 제목이 같아도 되는데 분류는 제목이 같으면 안됩니다.
    
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    # SlugField : 사람이 읽을 수 있는 텍스트로 고유의 url을 만들어준다(카테고리에서 pk 역할을 합니다.)
    # allow_unicode=True : 한글을 사용할 수 있도록 하겠다(기본적으로 한글을 지원하지 않기 때문임).
    
    # 출력
    def __str__(self):
        return self.name
    
    # 주소를 받음
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'
    
    # Catagorys를 복수형으로 바꾸기(텍스트 수정하기)
    class Meta:
        verbose_name_plural = 'Categories'

# 태그
class Tag(models.Model):
    name = models.CharField(max_length=50)    
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    
    # 출력
    def __str__(self):
        return self.name
    
    # 주소를 받음
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = MarkdownxField()
    
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    # 연도 폴더 만들고, 월/일 디렉토리를 만든다.
    # blank=True : 필수 항목이 아니다.
    
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    # on_delete: 연결되어 있던 User가 삭제될 때
    # ForeignKey: 다대일 관계를 정의
    # SET_NULL : 글은 남아있게 하는데 작성자 이름은 NULL
    
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    # ForeignKey : 일대다 관계, null=True : 빈 글 허용(분류를 선택 안해도 될 수 있도록)
    # on_delete=models.SET_NULL : 해당 카테고리가 삭제되어도 포스트는 유지시킬 것이다
    # blank=True : 입력이 공백이어도 된다.
    
    # 태그 category
    # ManyToManyField : 다대다
    tags = models.ManyToManyField(Tag, blank=True)
    
    def __str__(self):
        return f'[{self.pk}]{self.title}::{self.author}'
    
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    
    # 경로 제외한 파일명 받아오기
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    
    # 확장자 받아오기
    def get_file_exit(self):
        return self.get_file_name().split('.')[-1]
    
    # 마크다운
    def get_content_markdown(self):
        return markdown(self.content)
    
    
# author : 추후에 작성하겠습니다(12.08에 일부분 작성했습니다.)
# Create your models here.
