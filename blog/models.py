from django.db import models
from django.contrib.auth.models import User
import os

# DB 연동
# 1. 함수를 사용하는 방법
# 2. Class를 사용하는 방법

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    # 연도 폴더 만들고, 월/일 디렉토리를 만든다.
    # blank=True : 필수 항목이 아니다.
    
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # on_delete: 연결되어 있던 User가 삭제될 때
    # ForeignKey: 다대일 관계를 정의
    
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
    
    # author : 추후에 작성하겠습니다.
# Create your models here.
