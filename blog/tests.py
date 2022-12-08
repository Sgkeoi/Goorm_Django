from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
# 자체 DB 를 새로 만들어서 가상 공간에서 테스트 한다

class TestView(TestCase) :
    def setup(self) :
        self.client -= Client()
        # client = 컴퓨터 / 컴퓨터에서 테스트해서 날리면 -> goorm 에서 돌아간다
    
    def test_post_list(self) : # post_list 를 test 할 함수
        
        # 1.1 포스트 목록 페이지 가져오는지 확인
        response = self.client.get('/blog/')
        # 가상의 사용자가 /blob/ 를 쳤을 때 그걸 response 에 넣는다
        # /blog 해서 urls.py 가서 페이지 가져오는 행동이 잘 되고 있는지 확인하는 것
        
        # 1.2 정상적으로 페이지 로드되는지 확인
        self.assertEqual(response.status_code, 200)
        # 응답받은 response 의 상태코드가 200 과 같은가 ? -> 200 : 성공. 제대로 load 했다는 뜻
        # 페이지가 없으면 주로 404
        
        # 1.3 포스트 목록 페이지의 <title> 태그 중 'Blog' 가 있는지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # 현재 들어온 내용을 parser 로 나눠서 html 로 바꿔서 저장해주라
        self.assertEqual(soup.title.text, 'Blog')
        # title 의 text 가 Blog 와 같은가 ?
        
        # 1.4 <Nav> Navbar 가 있는지 확인
        navbar = soup.nav
        # soup 에 nav 가 있나 ? 결과는 navbar 에 들어감
        
        # 1.5 Blog , AboutMe 라는 문구가 네비게이션 바에 있는가
        self.assertIn('Blog', navbar.text )
        # assertIn() : 안에 있니 ?
        # Blog 라는 글자가 navbar 안에 있니 ? 
        self.assertIn('About Me', navbar.text)
        # About Me 라는 글자가 navbar 안에 있니 ?
        
        # --------------------------------------------------------------------------------
        
        # 2.1 포스트가 하나도 없는가 ? ( 여기는 가상의 DB 니까 내가 만들어놓은게 영향을 미치지 않는다 )
        self.assertEqual(Post.objects.count(), 0)
        # objects 를 셌을 때 0과 같으면 하나도 없다는 뜻
        
        # 2.2 main-area 에 '아직 게시물이 없습니다' 라는 문구가 나타난다.
        main_area = soup.find('div', id = "main-area")
        self.assertIn('아직 게시물이 없습니다', main_area.text)
        
        # --------------------------------------------------------------------------------
        # 미리 생각해두고 test 하고 구현한다
        
        # 3.1 포스트가 2개 있다면 ( 테스트하려고 2개를 강제로 만들었다 )
        post_001 = Post.objects.create(
            title = '첫번째 포스트 입니다.',
            content = 'Hello World. We are the World',
        )
        
        post_002 = Post.objects.create(
            title = '두번째 포스트 입니다.',
            content = '1등이 전부가 아니잖아요!',
        ) 
         
        self.assertEqual(Post.objects.count(), 2)
        # 이제 포스트 2개를 작성했으니까 objects 가 2개인지 확인해본다
        
        # 3.2 포스트 목록 페이지를 새로고침 했을 때
        # 가상의 클라이언트가 /blog/ 라고 쳐서 서버에 html 을 날렸다 -> 서버는 parser 한다
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        # response 안의 content의 html 을 parser 한다
        self.assertEqual(response.status_code, 200)
        # response 가 200 인가 ? ( 정상적으로 돌아왔냐 ) 
        
        # 3.3 main-area 에 포스트가 2개 존재한다
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        # 3.4 '아직 게시물이 없습니다' 라는 문구가 더 이상 나타나지 않는다.
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

    # ------------------------------------------------------------------------------------
        
    def test_test_detail(self) : # 매개변수로 받는게 없더라도 self 적어야함
                                 # 만약에 pk 도 같이 받는다 하면 self, pk 이렇게
        
        # 1.1 포스트 하나 생성하기
        post_001 = Post.objects.create(
            title = '첫번째 포스트 입니다.',
            content = 'Hello World. We are the World',
        )
        
        # 1.2 포스트 url은 ( 상세 페이지 주소 ) '/blog/1/' 이렇게 pk 가 붙어있다
        # 지금은 포스트 하나니까 1 넣어서 검사해볼거임
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')
        
        # --------------------------------------------------------------------------------
        
        # 2.  첫번째 포스트의 상세 페이지 검사하기
        # 2.1 첫번째 포스트의 url 로 접근하면 정상적으로 작동하는가
        response = self.client.get(post_001.get_absolute_url()) # 1.2 에서 검증한 blog/1 을 가져온다
        soup = BeautifulSoup(response.content, 'html.parser')   # response 안의 content의 html 을 parser 한다
        self.assertEqual(response.status_code, 200)
        
        # 2.2 포스트의 목록 페이지와 같은 navbar 가 붙어있는가
        navbar = soup.nav
        self.assertIn('Blog', navbar.text )
        self.assertIn('About Me', navbar.text)
        
        # 2.3 첫번째 포스트의 제목이 웹브라우저 탭 타이틀에 들어있는가
        self.assertIn(post_001.title, soup.title.text)
        
        # 2.4 첫번째 포스트의 제목이 포스트 영역에 있는가
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)
        
        # 2.5 첫번째 포스트의 작성자가 포스트 영역에 있는가 ( 지금은 아직 구현 X )
        
        # 2.6 첫번째 포스트의 내용이 포스트 영역에 있는가
        self.assertIn(post_001.content, post_area.text)
        # html parser 했으니까 text 로 적어주는거임
        
        # ( 나중에는 작성자가 제대로 나오는지 카테고리가 어떤 식으로 짜여있는지 댓글창은 구현됐는지 테스트 할 수 있다 )