# CBV 방식으로 변경하기
# from django.shortcuts import render
from django.views.generic import ListView, DetailView    # Detail을 불러오겠음
from .models import Post

class PostList(ListView):
    model = Post
    ordering = '-pk'
    # Post 나열
    # index 함수의 역할을 대신하게 된다.
    # Blog의 urls를 전부 수정해야 한다.
    
class PostDetail(DetailView):
    model = Post
    

# from django.shortcuts import render
# from .models import Post
 
# # 함수 방식으로 만들기
# # render : '템플릿'이라고 하는 폴더를 찾으러 감

# def index(request):
    
#     # objects.all() : DB Query 명령어
#     # DB에 있는 것들을 전부 가져온다.
    
#     posts = Post.objects.all().order_by('-pk')
    
    
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts':posts,
#         }
#     )

# # urls에서 views.single_post_page로 이동했음.
# # request와 pk를 보내야 함
#def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#    
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post':post, 
#        }
#     )
# # 들어온 pk의 값들을 가져오는 것임

# # Create your views here.

