from django.db import models

# DB 연동
# 1. 함수를 사용하는 방법
# 2. Class를 사용하는 방법

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    # 연도 폴더 만들고, 월/일 디렉토리를 만든다.
    # blank=True : 필수 항목이 아니다.
    
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)
    
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'[{self.pk}]{self.title}'
    
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    
    # author : 추후에 작성하겠습니다.
# Create your models here.
