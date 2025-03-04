# 1登陆
# 2注册
# 3评论接口（前端给邮箱和教室id）
# 4根据邮箱查询收藏列表
# 5根据邮箱查询预订历史
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
import hashlib
import re


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
        return JsonResponse({'code': 500, 'message': '服务器内部错误'}, status=500)
