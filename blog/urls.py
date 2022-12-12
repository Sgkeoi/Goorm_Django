from django.urls import path
from . import views
# . : 현재 디렉토리(blog->urls)

# 경로 urls.py -> index.py
urlpatterns = [
    path('tag/<str:slug>/',views.tag_page),
    path('<int:pk>/',views.PostDetail.as_view()),
    # path('<int:pk>/',views.single_post_page), 사용 안 함(PostDetail로 변경되었음)
    
    path('category/<str:slug>/',views.category_page),
#     views에 있는 category_page로 이동시킴
#     https://project-ztsct.run.goorm.io/blog/category/programming
#     programming만 분리해서 view.py의 category_page로 보냄    
    
    # path('', views.index), Class 형태로 변환되었기 때문에 주석 처리한다.
    path('',views.PostList.as_view()),
    # post_list.html 형태로 만든다.
]

