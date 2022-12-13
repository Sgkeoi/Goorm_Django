# CBV 방식으로 변경하기
# from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView    # Detail을 불러오겠음
# django -> views -> generic 안의 CreateView를 불러오겠음.

# 로그인 관련해서 django에서 지원해주는 라이브러리
# 로그인되어있을때만 보여줌
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# UserPassesTestMixin : 스태프

from .models import Post, Category, Tag
from django.shortcuts import render, redirect

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post # Post 모듈을 사용하겠음
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate,self).form_valid(form)
        else:
            return redirect('/blog/')

class PostList(ListView):
    model = Post
    ordering = '-pk'
    # Post 나열
    # index 함수의 역할을 대신하게 된다.
    # Blog의 urls를 전부 수정해야 한다.
    
    # None인 category가 몇 개가 있는가?
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
    
class PostDetail(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super(PostDetail,self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

# path('category/<str:slug>/',views.category_page),에서 옴
def category_page(request, slug):
    if slug == 'no_category':
        category = "미분류"    # 카테고리가 없으면 미분류
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list':post_list,    
            'categories':Category.objects.all(), # 카드를 채워준다.
            'no_category_post_count':Post.objects.filter(category=None).count(), # 미분류, 미분류 개수 알려줌  
            'category': category, # 제목 옆에 카테고리 이름이 붙는다.
        }
    )

# 태그 페이지
def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list':post_list,
            'tag':tag,
            'categories':Category.objects.all(),
            'no_category_post_count':Post.objects.filter(category=None).count(),
        }
    )

# category=category : category로 필터링 한 것만 가지고 온다.

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

