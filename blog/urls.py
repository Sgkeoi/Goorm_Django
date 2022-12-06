from django.urls import path
from . import views
# . : 현재 디렉토리(blog->urls)

# 경로 urls.py -> index.py
urlpatterns = [
    path('<int:pk>/',views.PostDetail.as_view()),
    # path('<int:pk>/',views.single_post_page), 사용 안 함(PostDetail로 변경되었음)
    
    # path('', views.index), Class 형태로 변환되었기 때문에 주석 처리한다.
    path('',views.PostList.as_view()),
    # post_list.html 형태로 만든다.
]

