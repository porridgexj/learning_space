import json
import math
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt

from learning_space.user.models import LearningSpace, Booking, Comment, User, Seat


def haversine(lon1, lat1, lon2, lat2):
    """
    计算两个经纬度之间的球面距离（单位：公里）
    """
    # 将十进制度数转换为弧度
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # 地球半径，单位为公里
    return c * r
# def haversine_distance(lat1, lon1, lat2, lon2):
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
#     R = 3958.8
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     return R * c

# 1. 查询教室列表接口（支持按距离/评分排序）
def classroom_list(request):
    sort_by = request.GET.get('sort_by', '')
    # 获取传入的经度和纬度参数
    lon_param = request.GET.get('longitude', None)
    lat_param = request.GET.get('latitude', None)

    try:
        user_lon = float(lon_param) if lon_param is not None else None
        user_lat = float(lat_param) if lat_param is not None else None
    except ValueError:
        user_lon, user_lat = None, None

    spaces = LearningSpace.objects.all()

    results = []
    for space in spaces:
        distance = None
        if user_lon is not None and user_lat is not None and space.longitude is not None and space.latitude is not None:
            distance = haversine(user_lon, user_lat, float(space.longitude), float(space.latitude))
        results.append({
            "id": space.id,
            "space_name": space.space_name,
            "description": space.description,
            "seat_num": space.seat_num,
            "left_seat_num": space.left_seat_num,
            "score": float(space.score),
            "status": space.get_status_display(),  # 'Open' 或 'Closed'
            "distance": distance
        })

    if sort_by == "distance" and user_lon is not None and user_lat is not None:
        # 如果距离可计算，则按照距离升序排序，距离为 None 的排在最后
        results.sort(key=lambda x: x["distance"] if x["distance"] is not None else float('inf'))
    elif sort_by == "rating":
        results.sort(key=lambda x: x["score"], reverse=True)
    else:
        # 默认按照评分降序
        results.sort(key=lambda x: x["score"], reverse=True)

    return JsonResponse(results, safe=False)


# 2. 根据教室ID查询教室详细信息
def classroom_detail(request, classroom_id):
    space = get_object_or_404(LearningSpace, pk=classroom_id)
    data = {
        "id": space.id,
        "space_name": space.space_name,
        "description": space.description,
        "seat_num": space.seat_num,
        "left_seat_num": space.left_seat_num,
        "score": float(space.score),
        "longitude": float(space.longitude) if space.longitude is not None else None,
        "latitude": float(space.latitude) if space.latitude is not None else None,
        "status": space.get_status_display(),
        "create_time": space.create_time,
        "img_cover": space.img_cover,
    }
    return JsonResponse(data)

# 3. 根据教室ID查询座位预定数据
def classroom_booking_list(request, classroom_id):
    # 获取教室对象
    space = get_object_or_404(LearningSpace, pk=classroom_id)

    # 生成全量座位列表：1 到 seat_num
    full_seat_list = list(range(1, space.seat_num + 1))

    now = timezone.now()

    # 查询最近一天内且当前时间小于预定结束时间的预定记录（视为占用）
    active_bookings = Booking.objects.filter(
        space_id=classroom_id,
        create_time__gte=now - timedelta(days=1),
        end_time__gt=now
    )
    # 收集预定记录中的座位号
    occupied_seats = set(b.seat_no for b in active_bookings)

    # 查询该教室所有 Seat 记录，收集维修中（status == 2）的座位号
    maintenance_seats = set()
    seat_objs = Seat.objects.filter(space=space)
    for seat in seat_objs:
        if seat.status == 2:
            maintenance_seats.add(seat.seat_no)

    # 构造返回的座位状态列表：每个对象包含 index 和 status
    seat_status_list = []
    for seat_no in full_seat_list:
        if seat_no in maintenance_seats:
            status = 2
        elif seat_no in occupied_seats:
            status = 1
        else:
            status = 0
        seat_status_list.append({"index": seat_no, "status": status})

    # 计算当前可用座位数量（状态为 0 的个数）
    available_count = sum(1 for seat in seat_status_list if seat["status"] == 0)

    # 更新 LearningSpace 表中的 left_seat_num 字段
    space.left_seat_num = available_count
    space.save(update_fields=["left_seat_num"])

    # 返回数据
    data = {
        "classroom_id": classroom_id,
        "seat_status_list": seat_status_list,
        "available_seat_count": available_count,
        # 如有需要，可同时返回部分有效预定记录信息
        "active_bookings": [
            {
                "seat_no": b.seat_no,
                "start_time": b.start_time,
                "end_time": b.end_time,
                "user_email": b.user.email if b.user else None,
            } for b in active_bookings
        ]
    }

    return JsonResponse(data)

# 4. 根据教室ID和用户email查询该教室全部评分和评论信息
def classroom_review_list(request, classroom_id):
    email = request.GET.get('email', '')
    reviews = Comment.objects.filter(space_id=classroom_id)
    if email:
        reviews = reviews.filter(user__email=email)
    review_data = []
    for r in reviews:
        review_data.append({
            "id": r.id,
            "user_email": r.user.email,
            "comment_description": r.comment_description,
            "score": float(r.score),
            "status": r.get_status_display(),  # 'Active', 'Deleted', 'Maintenance report'
            "create_time": r.create_time,
            "update_time": r.update_time,
        })
    data = {
        "classroom_id": classroom_id,
        "reviews": review_data
    }
    return JsonResponse(data)


# -------------------------------
# 预定座位接口
# URL: POST /api/v1/bookings
# 请求参数（JSON）： user_email, classroom_id, seat_no, start_time, end_time
# -------------------------------
@csrf_exempt
def book_seat(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    required_fields = ['user_email', 'classroom_id', 'seat_no', 'start_time', 'end_time']
    if not all(field in data for field in required_fields):
        return JsonResponse({"error": "Missing required parameters"}, status=400)

    # 获取用户
    try:
        user = User.objects.get(email=data['user_email'])
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    # 解析预定时间段
    start_time = parse_datetime(data['start_time'])
    end_time = parse_datetime(data['end_time'])
    if start_time is None or end_time is None:
        return JsonResponse({"error": "Invalid start_time or end_time"}, status=400)

    now = timezone.now()
    # 检查当前时间起未来两小时内是否已有该座位的预定记录
    active_existing = Booking.objects.filter(
        space_id=data['classroom_id'],
        seat_no=data['seat_no'],
        start_time__lt=now + timedelta(hours=2),
        end_time__gt=now
    )
    if active_existing.exists():
        return JsonResponse({"error": "Seat already booked within the next two hours"}, status=400)

    # 如果没有冲突，则创建预定记录
    booking = Booking.objects.create(
        user=user,
        space_id=data['classroom_id'],
        seat_no=data['seat_no'],
        start_time=start_time,
        end_time=end_time
    )

    return JsonResponse({
        "message": "Booking created successfully",
        "booking_id": booking.id
    })


def cancel_booking(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    booking_id = data.get("booking_id")
    if not booking_id:
        return JsonResponse({"error": "Missing booking_id"}, status=400)

    try:
        booking = Booking.objects.get(pk=booking_id)
    except Booking.DoesNotExist:
        return JsonResponse({"error": "Booking not found"}, status=404)

    booking.delete()
    return JsonResponse({"message": "Booking cancelled successfully"})


@csrf_exempt
def create_learning_space(request):
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    required_fields = ['space_name', 'seat_num', 'left_seat_num', 'score', 'longitude', 'latitude']
    if not all(field in data for field in required_fields):
        return JsonResponse({"error": "Missing required parameters"}, status=400)

    space = LearningSpace.objects.create(
        space_name=data['space_name'],
        description=data.get('description', ''),
        seat_num=data['seat_num'],
        left_seat_num=data['left_seat_num'],
        score=data['score'],
        longitude=data['longitude'],
        latitude=data['latitude'],
        status=data.get('status', 0),
        img_cover=data.get('img_cover', '')
    )
    return JsonResponse({
        "message": "Learning space created successfully",
        "learning_space_id": space.id
    })


@csrf_exempt
def update_learning_space(request, classroom_id):
    if request.method not in ['POST', 'PUT']:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        space = LearningSpace.objects.get(pk=classroom_id)
    except LearningSpace.DoesNotExist:
        return JsonResponse({"error": "Learning space not found"}, status=404)

    # 更新可修改的字段
    fields = ['space_name', 'description', 'seat_num', 'left_seat_num', 'score', 'longitude',
              'latitude', 'status', 'img_cover']
    for field in fields:
        if field in data:
            setattr(space, field, data[field])
    space.save()
    return JsonResponse({"message": "Learning space updated successfully"})