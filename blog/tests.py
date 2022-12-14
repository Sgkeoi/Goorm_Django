from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment

# ---------------------------------------------------------------------------------------------------------------

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')
        
        self.user_obama.is_staff = True # 오바마 계정은 스태프 권리를 가진다
        self.user_obama.save()
        
        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.tag_python_kor = Tag.objects.create(name="파이썬 공부", slug="파이썬-공부")
        self.tag_python = Tag.objects.create(name="python", slug="python")
        self.tag_hello = Tag.objects.create(name="hello", slug="hello")
        
        self.post_001 = Post.objects.create(
            title='첫번째 포스트입니다.',
            content='Hello World. We are the world.',
            category=self.category_programming,
            author=self.user_trump
        )
        self.post_001.tags.add(self.tag_hello)
        
        self.post_002 = Post.objects.create(
            title='두번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_music,
            author=self.user_obama
        )
        # post_002 에는 tag 추가 안함
        
        self.post_003 = Post.objects.create(
            title='세번째 포스트입니다.',
            content='category가 없을 수도 있죠',
            author=self.user_obama
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)
        
        # 댓글
        self.comment_001 = Comment.objects.create(
            post = self.post_001,
            author = self.user_obama,
            content = '첫 번째 댓글'
        )
        # 댓글은 post_detail.html에 달린다.

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)


        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

    
        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(
            f'{self.category_programming.name} ({self.category_programming.post_set.count()})',
            categories_card.text
        )
        self.assertIn(
            f'{self.category_music.name} ({self.category_music.post_set.count()})',
            categories_card.text
        )
        self.assertIn(f'미분류(1)', categories_card.text)

    def test_post_list(self):
        # Post가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual(soup.title.text, 'Blog')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')  # id가 post-1인 div를 찾아서, 그 안에
        self.assertIn(self.post_001.title, post_001_card.text)  # title이 있는지
        self.assertIn(self.post_001.category.name, post_001_card.text)  # category가 있는지
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)  # 작성자명이 있는지

        self.assertIn(self.tag_hello.name, post_001_card.text)
        # 태그 hello 가 post_001 에 있니 ?
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)
        # 위에서 001 에는 python, python_kor 은 안 넣어줬으니까 NotIn
        
        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.post_002.author.username.upper(), post_002_card.text)

        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)
        # 위에서 002 에는 아무 태그도 안 넣어줬으니까 NotIn
        
        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text)

        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        # 003 에는 hello 는 안 넣고, python 과 python_kor 태그는 넣어줬으니까 요렇게 ! 

        
        # Post가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')  # id가 main-area인 div태그를 찾습니다.
        self.assertIn('아직 게시물이 없습니다', main_area.text)

    
    def test_post_detail(self):
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        self.assertIn(self.user_trump.username.upper(), post_area.text)
        self.assertIn(self.post_001.content, post_area.text)
        
        # comment area
        comments_area = soup.find('div', id='comment-area')
        comment_001_area = comments_area.find('div', id='comment-1')
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        self.assertIn(self.comment_001.content, comment_001_area.text)
        

    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)
        
    def test_tag_page(self) :
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)
        
        self.assertIn(self.tag_hello.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)
        
    def test_create_post(self) :
        
        # 로그인이 안 된 상태
        response = self.client.get('/blog/create_post')
        self.assertNotEqual(response.status_code, 200)
        # 로그인이 안 된 상태니까 200이 뜨면 안 된다
        
        # trump 로그인하기
        self.client.login(username='trump', password='somepassword')
        response = self.client.get('/blog/create_post')
        # trump 계정이 로그인해서 create_post 로 들어갔다
        self.assertNotEqual(response.status_code, 200)
        # 얘는 권한이 없으니까 200 뜨면 안 된당        
        
        # obama 로그인 하기 - obama 는 관리자 계정
        self.client.login(username='obama', password='somepassword')
        
        # 로그인이 된 상태
        response = self.client.get('/blog/create_post/')
        # 가상의 사용자 client 가 주소창에 /blog/create_post/ 라고 치고 들어오면
        
        self.assertEqual(response.status_code, 200)
        # 제대로 들어왔다면 200 이 뜬다
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # 들어온 내용 중 html 을 찾아서 soup 에 넣어주기
        
        self.assertEqual('Create Post - Blog', soup.title.text )
        # 페이지에 들어가있는 내용 확인 ( 페이지로 잘 들어갔는지 확인할 수 있다 )
        
        main_area = soup.find('div', id='main-area')
        # div 중 id 가 main-area 인 것을 찾아서 main_area 변수에 넣기
        
        self.assertIn('Create New Post', main_area.text)
        # Create new Post 가 main_area 에 있는지 확인
        
        # 태그 입력 테스트
        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        
        self.client.post( # submit 눌렀을 때의 페이지 테스트
            '/blog/create_post/',
            {
                'title' : 'Post Form 만들기',
                'content' : 'Post Form 페이지를 만듭시다.',
                'tags_str' : 'new tag; 한글 태그, python'
            }
        )
        # test 서버 안에 만든 게시물
        
        last_post = Post.objects.last()
        # 가장 최근의 게시글
        
        self.assertEqual(last_post.title, "Post Form 만들기")
        # 만든 게시물 확인
        
        self.assertEqual(last_post.author.username, 'obama')
        # 마지막 게시물을 작성한 사람이 obama 가 맞니
        
        self.assertEqual(last_post.tags.count(),3)
        # 태그가 3개 있는가
        
        self.assertTrue(Tag.objects.get(name='new tag'))
        # 'new tag'가 있는가
        
        self.assertTrue(Tag.objects.get(name='한글 태그'))
        # '한글 태그'가 있는가
        
    def test_update_post(self) :
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'
        # test 안에서 만든 003번째 pk ( 아마도 3 ) 을 넣어 불러오기
        
        # 아직 로그인을 안 했음
        response = self.client.get(update_post_url)
        # 로그인이 안 된 경우니까 200 이 뜨면 안 된다
        self.assertNotEqual(response.status_code, 200)
        
        # 로그인을 했지만 작성자가 아닌 경우
        self.assertNotEqual(self.post_003.author, self.user_trump)
        # 3번을 작성한 작성자는 obama임 -> trump 가 작성한 게 아니니까 NotEqual 맞음
        
        self.client.login(
            username = self.user_trump.username,
            password = 'somepassword'
        )
        
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)
        # 403 : 권한 없음 코드
        # trump 가 작성한 게시물이 아니라서 403 코드가 나온다
        
        
        # 작성자 본인이 로그인 한 경우
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)

        self.client.login(
            username = self.post_003.author.username,
            password = 'somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        # 이제 작성자 본인이 들어왔으니까 200 코드가 뜬당
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)
        
        # 컨텐츠 삽입
        response = self.client.post(
            update_post_url,
            {
                'title' : '세번째 포스트를 수정했습니다.' ,
                'content' : '안녕 세계! 우리는 하나?' ,
                'category' : self.category_music.pk
            },
            follow = True
        )
        
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('세번째 포스트를 수정했습니다.', main_area.text )
        self.assertIn('안녕 세계! 우리는 하나?', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)
        
    def test_comment_form(self):
        self.assertEqual(Comment.objects.count(),1)
        # 댓글이 1개 있는가?
        
        self.assertEqual(self.post_001.comment_set.count(),1)
        # post_001에 댓글이 1개 있는가?
        
        # 로그인을 하지 않은 상태
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content,'html.parser')
        
        comment_area = soup.find('div', id='comment-area')
        self.assertIn('Log in and Leave a Comment', comment_area.text)
        self.assertFalse(comment_area.find('form',id='comment-form'))
        # 로그인하지 않으면 form을 보여주지 않음
        
        # 로그인을 한 상태
        self.client.login(username='obama', password='somepassword')
        # 클라이언트에서 로그인을 하는데 username이 'obama'이고 비밀번호가 'somepassword'인 경우
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content,'html.parser')
        
        comment_area = soup.find('div', id='comment-area')
        self.assertNotIn('Log in and Leave a Comment', comment_area.text)
        
        comment_form = comment_area.find('form', id='comment-form')
        #self.assertTrue(comment.form.find('textarea', id='id_content'))
        
        response = self.client.post(
            self.post_001.get_absolute_url() + 'new_comment/',
            {
                'content':'오바마의 댓글입니다.',
            },
            follow = True
        )
        
        # 댓글의 응답이 제대로 왔는지 확인하기
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)
        
        new_comment = Comment.objects.last()
        
        soup = BeautifulSoup(response.content,'html.parser')
        self.assertIn(new_comment.post.title,soup.title.text)
        
        comment_area = soup.find('div', id='comment-area')
        new_comment_div = comment_area.find('div', id=f'comment-{new_comment.pk}')
        self.assertIn('obama', new_comment_div.text)
        self.assertIn('오바마의 댓글입니다.', new_comment_div.text)
    
    # 댓글 테스트
    def test_comment_update(self):
        comment_by_trump = Comment.objects.create(
            post = self.post_001,
            author = self.user_trump,
            content = '트럼프의 댓글입니다.'
        )
    
        # 로그인이 안 된 상태
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a',id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a',id='comment-2-update-btn'))

        # 작성자가 아닌 계정이 로그인
        self.client.login(username='obama', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a',id='comment-2-update-btn'))
        comment_001_update_btn = comment_area.find('a', id='comment-1-update-btn')
        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')
        
        
        # edit 버튼이 있다고 가정하고 테스트
        response = self.client.get('/blog/update_comment/1/')
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        
        self.assertEqual('Edit Comment - Blog', soup.title.text)
        update_comment_form = soup.find('form', id='comment-form')
        content_textarea = update_comment_form.find('textarea', id='id_content')
        self.assertIn(self.comment_001.content,content_textarea.text)
        
        response = self.client.post(
            f'/blog/update_comment/{ self.comment_001.pk }/',
            {
                'content':"오바마의 댓글을 수정합니다."
            },
            follow = True
            # follow = True : 끝나면 절대경로로 redirection한다.
        )
        
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        comment_001_div = soup.find('div', id='comment-1')
        self.assertIn("오바마의 댓글을 수정합니다.",comment_001_div.text)
        self.assertIn("Update: ",comment_001_div.text)
    
    # 댓글 삭제 기능 테스트
    def test_delete_comment(self):
        comment_by_trump = Comment.objects.create(
            post = self.post_001,
            author = self.user_trump,
            content = '트럼프의 댓글입니다.'
        )
        self.assertEqual(Comment.objects.count(),2)
        self.assertEqual(self.post_001.comment_set.count(),2)
        
        # 로그인 하지 않은 상태(delete 버튼 없어야 함)
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        
        comment_area = soup.find('div',id='comment-area')
        self.assertFalse(comment_area.find('a',id='comment-1-delete-btn'))
        self.assertFalse(comment_area.find('a',id='comment-2-delete-btn'))
        
        # 로그인 한 상태(trump가 로그인)
        self.client.login(username='trump',password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        
        comment_area = soup.find('div',id='comment-area')
        self.assertFalse(comment_area.find('a',id='comment-1-delete-btn'))
        comment_002_delete_modal_btn = comment_area.find('a', id='comment-2-delete-modal-btn')
        self.assertIn('delete',comment_002_delete_modal_btn.text) # delete 버튼을 만들고 그 안에 text를 넣는다.
        self.assertEqual(comment_002_delete_modal_btn.attrs['data-target'], '#deleteCommentModal-2') # attrs : 중복이 있는가
        
        delete_comment_modal_002 = soup.find('div', id='deleteCommentModal-2')
        self.assertIn('댓글을 삭제하시겠습니까?', delete_comment_modal_002.text)  # 구현할 때도 똑같아야 한다.
        really_delete_btn_002 = delete_comment_modal_002.find('a')
        self.assertIn('Delete',really_delete_btn_002.text)
        self.assertEqual(really_delete_btn_002.attrs['href'],'/blog/delete_comment/2/')
        
        response = self.client.get('/blog/delete_comment/2/', follow=True)
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        self.assertIn(self.post_001.title,soup.title.text)
        comment_area = soup.find('div', id=='comment_area')
        self.assertNotIn('트럼프의 댓글입니다.', comment_area.text)
        
        self.assertEqual(Comment.objects.count(),1)
        self.assertEqual(self.post_001.comment_set.count(),1)