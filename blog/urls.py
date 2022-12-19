from django.urls import path
from . import views
# . : 현재 디렉토리(blog->urls)

# 경로 urls.py -> index.py
urlpatterns = [
    path('search/<str:q>/',views.PostSearch.as_view()),  # 글 검색하기
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    
    path('tag/<str:slug>/',views.tag_page),
    path('<int:pk>/',views.PostDetail.as_view()),
    # path('<int:pk>/',views.single_post_page), 사용 안 함(PostDetail로 변경되었음)
    
    path('category/<str:slug>/',views.category_page),
#     views에 있는 category_page로 이동시킴
#     https://project-ztsct.run.goorm.io/blog/category/programming
#     programming만 분리해서 view.py의 category_page로 보냄 
    
    path('<int:pk>/new_comment/', views.new_comment),
    
    # path('', views.index), Class 형태로 변환되었기 때문에 주석 처리한다.
    path('',views.PostList.as_view()),
    # post_list.html 형태로 만든다.
]

