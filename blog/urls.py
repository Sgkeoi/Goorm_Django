from django.urls import path
from . import views
# . : 현재 디렉토리(blog->urls)

# 경로 urls.py -> index.py
urlpatterns = [
    path('<int:pk>/',views.single_post_page),
    # views.single_post_page로 이동한다.
    
    path('', views.index),
]

