from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from learning_space.user.models import LearningSpace, User, Booking, Comment, Seat
import json

class SpaceAPITestCase(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create(
            email='test@example.com',
            password='testpassword',
            nickname='Test User'
        )
        
        # 创建测试学习空间
        self.space = LearningSpace.objects.create(
            space_name='Test Space',
            description='Test Description',
            seat_num=10,
            left_seat_num=10,
            score=Decimal('4.5'),
            longitude=Decimal('116.3'),
            latitude=Decimal('39.9'),
            status=1,  # 假设1代表开放状态
            img_cover='test.jpg'
        )
        
        # 创建测试座位
        self.seat = Seat.objects.create(
            space=self.space,
            seat_no=1,
            status=1  # 假设1代表正常状态
        )
        
        # 创建测试预订
        self.booking = Booking.objects.create(
            user=self.user,
            space=self.space,
            seat_no=1,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=2)
        )
        
        # 创建测试评论
        self.comment = Comment.objects.create(
            user=self.user,
            space=self.space,
            comment_description='Test Comment',
            score=Decimal('4.5'),
            status=1  # 假设1代表有效状态
        )
        
        self.client = Client()
    
    def test_classroom_list(self):
        # 测试默认排序
        response = self.client.get(reverse('classroom-list'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data) > 0)
        
        # 测试按评分排序
        response = self.client.get(reverse('classroom-list') + '?sort_by=rating')
        self.assertEqual(response.status_code, 200)
        
        # 测试按距离排序
        response = self.client.get(
            reverse('classroom-list') + 
            '?sort_by=distance&longitude=116.4&latitude=39.9'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_classroom_detail(self):
        response = self.client.get(
            reverse('classroom-detail', args=[self.space.id])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['space_name'], 'Test Space')
        self.assertEqual(data['description'], 'Test Description')
        
        # 测试不存在的教室ID
        response = self.client.get(
            reverse('classroom-detail', args=[99999])
        )
        self.assertEqual(response.status_code, 404)
    
    def test_classroom_booking_list(self):
        response = self.client.get(
            reverse('classroom-bookings', args=[self.space.id])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('seat_status_list', data)
        self.assertIn('available_seat_count', data)
        self.assertIn('active_bookings', data)
    
    def test_classroom_review_list(self):
        # 测试获取所有评论
        response = self.client.get(
            reverse('classroom-reviews', args=[self.space.id])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('reviews', data)
        
        # 测试按用户筛选评论
        response = self.client.get(
            reverse('classroom-reviews', args=[self.space.id]) +
            f'?email={self.user.email}'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(len(data['reviews']) > 0)
    
    def test_book_seat(self):
        # 测试成功预订座位
        booking_data = {
            'user_email': self.user.email,
            'classroom_id': self.space.id,
            'seat_no': 2,
            'start_time': (timezone.now() + timedelta(hours=1)).isoformat(),
            'end_time': (timezone.now() + timedelta(hours=3)).isoformat()
        }
        response = self.client.post(
            reverse('book-seat'),
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # 测试无效的请求数据
        invalid_data = {
            'user_email': self.user.email,
            'classroom_id': self.space.id
            # 缺少必要字段
        }
        response = self.client.post(
            reverse('book-seat'),
            data=json.dumps(invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_cancel_booking(self):
        # 测试成功取消预订
        cancel_data = {
            'booking_id': self.booking.id
        }
        response = self.client.post(
            reverse('cancel-booking'),
            data=json.dumps(cancel_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        # 测试取消不存在的预订
        invalid_cancel_data = {
            'booking_id': -1
        }
        response = self.client.post(
            reverse('cancel-booking'),
            data=json.dumps(invalid_cancel_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)