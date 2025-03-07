from django.urls import path,include
from . import api_views
from django.contrib import admin

space_urls = [
    # 1. 查询教室列表接口（支持 sort_by=distance 或 sort_by=rating）
    path('api/v1/classrooms', api_views.classroom_list, name='classroom-list'),
    # 2. 根据教室ID查询教室详细信息
    path('api/v1/classrooms/<int:classroom_id>', api_views.classroom_detail, name='classroom-detail'),
    # 3. 根据教室ID查询座位预定数据
    path('api/v1/classrooms/<int:classroom_id>/bookings', api_views.classroom_booking_list, name='classroom-bookings'),
    # 4. 根据教室ID和用户email查询该教室全部评分和评论信息
    path('api/v1/classrooms/<int:classroom_id>/reviews', api_views.classroom_review_list, name='classroom-reviews'),
    # 预定座位接口
    path('api/v1/bookings', api_views.book_seat, name='book-seat'),
    # 取消座位接口
    path('api/v1/bookings/cancel', api_views.cancel_booking, name='cancel-booking'),
    # 创建学习空间接口
    path('api/v1/learning_spaces/create', api_views.create_learning_space, name='create-learning-space'),
    # 修改学习空间细节接口
    path('api/v1/learning_spaces/<int:classroom_id>/update', api_views.update_learning_space, name='update-learning-space'),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('learning_space.user.api_urls')),  
]


