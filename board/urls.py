from django.urls import path
from . import views
# 현재 디렉토리에서 views로 간다.

urlpatterns = [
    path('create/',views.BoardCreate.as_view()),
    path('<int:pk>/',views.BoardDetail.as_view()),
    path('',views.BoardList.as_view()),
]

# 메뉴 추가
# start app
# models 추가
# settings 추가(board)
# migration
# admin추가
# 게시판에 글 올리기(테스트용)
# urls에 추가
# views에 추가
