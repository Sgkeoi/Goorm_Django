from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
# 데이터베이스를 새로 만들어서 test를 진행한다.

# Create your tests here.

# TestCase에서 상속받아옴
class TestView(TestCase):
    def setup(self):
        self.client -= Client()
    
    def test_post_list(self):
        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        # /blog -> urls.py에서 페이지를 잘 가지고 오는지 확인하기
        
        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # response의 코드가 200(성공)인가?
        
        # 1.3 페이지 타이틀 태그가 'Blog'인지 확인한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        # 현재 들어오는 내용들을 'html.parser'로 변경하라
        self.assertEqual(soup.title.text,'Blog')
        # title의 text가 'Blog'인가?
        
        # 1.4 내비게이션 바가 존재하는지 확인한다.
        navbar = soup.nav
        # soup에 navbar가 있는가?
        
        # 1.5 Blog와 About_Me라는 문구가 내비게이션 바에 있다.
        # 
        self.assertIn('Blog',navbar.text)
        self.assertIn('About Me',navbar.text)
        # assertIn() : 이 안에 있는가?
        # Blog와 About_Me라는 문구가 내비게이션 바 안에 있는가?
