# 1登陆
# 2注册
# 3评论接口（前端给邮箱和教室id）
# 4根据邮箱查询收藏列表
# 5根据邮箱查询预订历史
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import User, FavouriteSpace, Booking, Comment, LearningSpace
from django.db.models import Avg
import json
import hashlib
import re



def hash_password(password):
    """对密码进行 SHA-256 加密"""
    return hashlib.sha256(password.encode()).hexdigest()

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '')
        password = data.get('password', '')
        nickname = data.get('nickname', '')

        # 参数验证
        if not all([email, password, nickname]):
            return JsonResponse({'code': 400, 'message': '请填写所有必填字段'}, status=400)

        # 邮箱格式验证
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return JsonResponse({'code': 400, 'message': '邮箱格式不正确'}, status=400)

        # 检查邮箱是否已注册
        if User.objects.filter(email=email).exists():
            return JsonResponse({'code': 400, 'message': '该邮箱已被注册'}, status=400)

        # 密码长度验证
        if len(password) < 6:
            return JsonResponse({'code': 400, 'message': '密码长度不能少于6位'}, status=400)

        # 密码加密
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # 创建用户
        user = User.objects.create(
            email=email,
            password=password_hash,
            nickname=nickname
        )

        return JsonResponse({
            'code': 200,
            'message': '注册成功',
            'data': {
                'user_id': user.id,
                'email': user.email,
                'nickname': user.nickname
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({'code': 400, 'message': '无效的请求数据格式'}, status=400)
    
    except Exception as e:
        return JsonResponse({'code': 500, 'message': f'服务器内部错误: {str(e)}'}, status=500)



@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """用户登录 API"""
    try:
        data = json.loads(request.body)  # 获取 JSON 数据
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        # 1. 校验必填字段
        if not all([email, password]):
            return JsonResponse({'code': 400, 'message': '请填写所有必填字段'}, status=400)

        # 2. 加密密码进行匹配
        password_hash = hash_password(password)

        # 3. 查询用户
        user = User.objects.filter(email=email, password=password_hash).first()
        if user:
            return JsonResponse({
                'code': 200,
                'message': '登录成功',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'nickname': user.nickname
                }
            })
        else:
            return JsonResponse({'code': 401, 'message': '邮箱或密码错误'}, status=401)


    except json.JSONDecodeError:
        return JsonResponse({'code': 400, 'message': '无效的请求数据格式'}, status=400)
    except Exception as e:
        return JsonResponse({'code': 500, 'message': '服务器内部错误'}, status=500)
    

    


@csrf_exempt
@require_http_methods(["GET"])
def get_favourite_spaces(request):
    """根据邮箱查询用户收藏的学习空间列表"""
    email = request.GET.get('email', '').strip()  # 从 GET 请求获取 email 参数

    if not email:
        return JsonResponse({'code': 400, 'message': '邮箱不能为空'}, status=400)

    try:
        user = User.objects.get(email=email)  # 查询用户
    except User.DoesNotExist:
        return JsonResponse({'code': 404, 'message': '用户不存在'}, status=404)

    # 获取该用户的收藏学习空间列表
    favourites = FavouriteSpace.objects.filter(user=user, status=0).values(
        'id', 'space__id', 'space__space_name', 'create_time'
    )

    return JsonResponse({
        'code': 200,
        'message': '查询成功',
        'data': list(favourites)
    })


@require_http_methods(["GET"])
def get_booking_history(request):
    """根据邮箱查询用户的预订历史"""
    email = request.GET.get('email', '').strip()

    if not email:
        return JsonResponse({'code': 400, 'message': '邮箱不能为空'}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'code': 404, 'message': '用户不存在'}, status=404)

    bookings = Booking.objects.filter(user=user).values(
        'id', 'space__id', 'space__space_name', 'start_time', 'end_time', 'seat_no', 'create_time'
    ).order_by('-start_time')  # 按预订开始时间排列

    return JsonResponse({
        'code': 200,
        'message': '查询成功',
        'data': list(bookings)
    })


@csrf_exempt
@require_http_methods(["POST"])
def submit_comment(request):
    """提交评论接口"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        space_id = data.get('space_id', '')
        score = data.get('score', '')
        comment_description = data.get('comment', '').strip()

        # 1. 验证必填字段
        if not all([email, space_id, score, comment_description]):
            return JsonResponse(
                {'code': 400, 'message': '缺失必填字段：邮箱、教室ID、评分、评论内容'},
                status=400
            )

        # 2. 验证评分范围
        try:
            score = float(score)
            if not (1 <= score <= 5):
                raise ValueError
        except ValueError:
            return JsonResponse(
                {'code': 400, 'message': '评分必须是1到5之间的数字'},
                status=400
            )

        # 3. 查询用户和教室
        try:
            user = User.objects.get(email=email)
            space = LearningSpace.objects.get(id=space_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'code': 404, 'message': '用户或教室不存在'},
                status=404
            )

        # 4. 创建评论
        comment = Comment.objects.create(
            user=user,
            space=space,
            comment_description=comment_description,
            score=score,
            status=0  # 默认状态为 Active
        )

        # 5. 返回成功响应
        return JsonResponse({
            'code': 200,
            'message': '评论提交成功',
            'data': {
                'comment_id': comment.id,
                'user_email': user.email,
                'space_id': space.id,
                'score': comment.score,
                'comment': comment.comment_description,
                'create_time': comment.create_time.strftime("%Y-%m-%d %H:%M:%S")
            }
        })
    
    except json.JSONDecodeError:
        return JsonResponse(
            {'code': 400, 'message': '无效的JSON格式'},
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {'code': 500, 'message': f'服务器内部错误: {str(e)}'},
            status=500
        )
    
@require_http_methods(["GET"])
def get_comments(request):
    """查询用户对特定学习空间的评论"""
    email = request.GET.get('email', '').strip()
    space_id = request.GET.get('space_id', '').strip()

    if not email or not space_id:
        return JsonResponse({'code': 400, 'message': '邮箱和学习空间 ID 不能为空'}, status=400)

    comments = Comment.objects.filter(user__email=email, space__id=space_id, status=0).values(
        'id', 'comment_description', 'score', 'create_time'
    )

    # 计算该学习空间的平均评分
    average_score = Comment.objects.filter(space__id=space_id, status=0).aggregate(Avg('score'))['score__avg']

    return JsonResponse({
        'code': 200,
        'message': '查询成功',
        'data': list(comments),
        'average_score': round(average_score, 2) if average_score else None  # 四舍五入保留两位小数
    })
    

