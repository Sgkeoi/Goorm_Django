from django.urls import path
from . import views

urlpatterns = [
    path('about_me/',views.about_me),
    path('', views.landing),
    # about_me와 landing은 만들어야 한다.
    # view에서 2개의 함수를 만들어줘야 한다.   
]

