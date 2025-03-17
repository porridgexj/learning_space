from django.test import TestCase, Client
from django.urls import reverse
from learning_space.user.models import User, LearningSpace, FavouriteSpace, Comment, Booking
import json
from learning_space.user.api_views import hash_password

class UserAPITestCase(TestCase):
    def setUp(self):
        """初始化测试用户和学习空间"""
        self.client = Client()
        self.test_email = "test@example.com"
        self.test_password = "securepass" # 原始密码
        self.test_nickname = "TestUser"
        
        # 创建测试用户（密码哈希处理）
        hashed_password = hash_password(self.test_password)
        self.user = User.objects.create(
            email=self.test_email, 
            password=hashed_password,  # 存储哈希后的密码
            nickname=self.test_nickname
        )

        # 创建一个学习空间
        self.space = LearningSpace.objects.create(space_name="Library", seat_num=50, left_seat_num=50)

    def test_register_user(self):
        """测试用户注册"""
        response = self.client.post(
            reverse("register"),
            data=json.dumps({
                "email": "newuser@example.com",
                "password": "securepass",
                "nickname": "NewUser"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_id", response.json()["data"])

    def test_register_existing_user(self):
        """测试注册已存在用户"""
        response = self.client.post(
            reverse("register"),
            data=json.dumps({
                "email": self.test_email,
                "password": "securepass",
                "nickname": "NewUser"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_login_valid_user(self):
        """测试正确的用户登录"""
        response = self.client.post(
            reverse("login"),
            data=json.dumps({
                "email": self.test_email,
                "password": self.test_password # 提交原始密码，视图会自动哈希
            }),
            
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("auth", response.cookies)  # 确保 cookies 里有 auth token

    def test_login_invalid_password(self):
        """测试使用错误密码登录"""
        response = self.client.post(
            reverse("login"),
            data=json.dumps({
                "email": self.test_email,
                "password": "wrongpassword"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
    # 先登录
     login_response = self.client.post(
        reverse("login"),
        data=json.dumps({
            "email": self.test_email,
            "password": self.test_password
        }),
        content_type="application/json"
    )
     self.client.cookies = login_response.cookies  # 保存Cookie
    
    # 再登出
     response = self.client.post(reverse("logout"))
     self.assertEqual(response.status_code, 200)


    def test_add_favourite_space(self):
        """测试添加学习空间到收藏列表"""
        # 先登录以获取Cookie
        login_response = self.client.post(
            reverse("login"),
            data=json.dumps({
                "email": self.test_email,
                "password": self.test_password
            }),
            content_type="application/json"
        )
        self.client.cookies = login_response.cookies
        
        response = self.client.post(
            reverse("add_favourite_space"),  
            data=json.dumps({
                "userid": self.user.id,  # 参数名改为userid
                "spaceid": self.space.id
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(FavouriteSpace.objects.filter(user=self.user, space=self.space).exists())

    def test_get_favourites(self):
        """测试获取用户收藏的学习空间"""
        FavouriteSpace.objects.create(user=self.user, space=self.space)
        # 先登录
        login_response = self.client.post(
            reverse("login"),
            data=json.dumps({
                "email": self.test_email,
                "password": self.test_password
            }),
            content_type="application/json"
        )
        self.client.cookies = login_response.cookies
        
        response = self.client.get(reverse("get_favourite_spaces"), {"id": self.user.id})  # 参数改为id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 1)

    def test_submit_comment(self):
        """测试提交学习空间评论"""
        # 先登录
        login_response = self.client.post(
            reverse("login"),
            data=json.dumps({
                "email": self.test_email,
                "password": self.test_password
            }),
            content_type="application/json"
        )
        self.client.cookies = login_response.cookies
        
        response = self.client.post(
            reverse("submit_comment"),
            data=json.dumps({
                "email": self.test_email,
                "space_id": self.space.id,
                "score": 4,
                "comment": "Great space!"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(user=self.user, space=self.space).exists())

    def test_get_comments(self):
        """测试获取学习空间的评论"""
    # 创建一条评论
        Comment.objects.create(
          user=self.user,
          space=self.space,
          comment_description="Great space!",
          score=5,
          status=0  #必须设置为 Active 状态
        )
    
    # 先登录
        login_response = self.client.post(
        reverse("login"),
        data=json.dumps({
            "email": self.test_email,
            "password": self.test_password
        }),
        content_type="application/json"
     )
        self.client.cookies = login_response.cookies
    
    # 再获取评论
        response = self.client.get(reverse("get_comments"), {"space_id": self.space.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 1)


    def test_get_booking_history(self):
        """测试获取用户预订历史"""
        Booking.objects.create(
            user=self.user,
            space=self.space,
            start_time="2024-04-01T10:00:00Z",
            end_time="2024-04-01T12:00:00Z",
            seat_no=1
        )
        # 先登录
        login_response = self.client.post(
            reverse("login"),
            data=json.dumps({
                "email": self.test_email,
                "password": self.test_password
            }),
            content_type="application/json"
        )
        self.client.cookies = login_response.cookies
        
        response = self.client.get(reverse("get_booking_history"), {"id": self.user.id})  # 参数改为id
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 1)
