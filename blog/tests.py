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
        # 설명 : 가상의 사용자가 주소를 입력하고 블로그를 시작하면 그것을 response에 넣는다.
        
        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # response의 코드가 200(성공)인가?
        # 설명 : 상태 코드가 정상적이면 200(성공)이 넘어온다. 찾을 수 없으면 404 에러가 나올 것이다.
        
        # 1.3 페이지 타이틀 태그가 'Blog'인지 확인한다.
        soup = BeautifulSoup(response.content, 'html.parser')
        # 현재 들어오는 내용들을 'html.parser'로 변경하라
        self.assertEqual(soup.title.text,'Blog')
        # title의 text가 'Blog'인가?
        # 설명 : parser로 바꾼 내용이 'Blog'인가?
        
        # 1.4 내비게이션 바가 존재하는지 확인한다.
        navbar = soup.nav
        # soup에 navbar가 있는가?
        
        # 1.5 Blog와 About_Me라는 문구가 내비게이션 바에 있다.
        self.assertIn('Blog',navbar.text)
        self.assertIn('About Me',navbar.text)
        # assertIn() : 이 안에 있는가?
        # Blog와 About_Me라는 문구가 내비게이션 바 안에 있는가?
        # 설명 : navbar에 'Blog'와 'About Me'라는 문구가 있는가?
        
        # 2.1 포스트가 하나도 없는가?(가상환경임)
        self.assertEqual(Post.objects.count(), 0)
        # objects.count() 0 : 하나도 없다.
        
        # 2.2 main area에 '아직 게시물이 없습니다.'라는 문구가 나타난다.
        # 어떤 방식으로 구현할지를 정하는 것이다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)
        
        # 3.1 포스트가 2개 있다면(테스트용으로 2개를 임의로 만든 것임)
        post_001 = Post.objects.create(
            title = '첫 번째 포스트입니다.',
            content = 'Hello World. We are the world.',
        )
        
        post_002 = Post.objects.create(
            title = '두 번째 포스트입니다.',
            content = '다 울었니? 이제 할 일을 하자.',
        )
        
        self.assertEqual(Post.objects.count(), 2)
        # Post를 2개 작성했으니 objects가 2개인지 확인
        
        # 3.2 포스트 목록 페이지를 새로고침했을때
        response = self.client.get('/blog/')
        # 설명 : 가상의 사용자가 주소를 입력하고 블로그를 시작하면 그것을 response에 넣는다.
        soup = BeautifulSoup(response.content,'html.parser')
        # 현재 들어오는 내용들을 'html.parser'로 변경하라
        self.assertEqual(response.status_code, 200)
        # response의 코드가 일치하면 200(성공)
        
        # 3.3 main area에 포스트가 2개 존재한다.
        main_area = soup.find('div',id='main-area')
        self.assertIn(post_001.title,main_area.text)
        self.assertIn(post_002.title,main_area.text)
        
        # 3.4 '아직 게시물이 없습니다'라는 문구는 더 이상 나타나지 않는다.
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)
        
        