from django.shortcuts import render
from .models import Post
 
# 함수 방식으로 만들기
# render : '템플릿'이라고 하는 폴더를 찾으러 감

def index(request):
    
    # objects.all() : DB Query 명령어
    # DB에 있는 것들을 전부 가져온다.
    
    posts = Post.objects.all().order_by('-pk')
    
    
    return render(
        request,
        'blog/index.html',
        {
            'posts':posts,
        }
    )

# Create your views here.

