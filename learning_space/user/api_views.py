from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import User, FavouriteSpace, Booking, Comment, LearningSpace
from django.db.models import Avg
import json
import hashlib
import re
from learning_space.utils import generate_token


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        email = data.get("email", "")
        password = data.get("password", "")
        nickname = data.get("nickname", "")

        if not all([email, password, nickname]):
            return JsonResponse(
                {"code": 400, "message": "Please fill in all required fields"},
                status=400,
            )

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            return JsonResponse(
                {"code": 400, "message": "Invalid email format"}, status=400
            )

        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"code": 400, "message": "This email has already been registered"},
                status=400,
            )

        if len(password) < 6:
            return JsonResponse(
                {"code": 400, "message": "Password must be at least 6 characters long"},
                status=400,
            )

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = User.objects.create(
            email=email, password=password_hash, nickname=nickname
        )

        return JsonResponse(
            {
                "code": 200,
                "message": "注册成功",
                "data": {
                    "user_id": user.id,
                    "email": user.email,
                    "nickname": user.nickname,
                },
            }
        )

    except json.JSONDecodeError:
        return JsonResponse({"code": 400, "message": "Invalid request"}, status=400)

    except Exception as e:
        return JsonResponse({"code": 500, "message": "error"}, status=500)


@require_http_methods(["POST"])
def login(request):
    print(request.body)
    try:
        data = json.loads(request.body)
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        if not all([email, password]):
            return JsonResponse({"code": 400, "message": "missing fields"}, status=400)
        password_hash = hash_password(password)
        user = User.objects.filter(email=email, password=password_hash).first()
        if user:
            token = generate_token(user.id)
            response = JsonResponse(
                {
                    "code": 200,
                    "message": "ok",
                    "data": {
                        "userid": user.id,
                        "email": user.email,
                        "nickname": user.nickname,
                    },
                }
            )
            response.set_cookie(
                key="auth",
                value=token,
                httponly=True,
                samesite="Lax",
                max_age=7 * 24 * 60 * 60,
            )
            return response
        else:
            return JsonResponse({"code": 401, "message": "invalid auth"}, status=401)
    except json.JSONDecodeError:
        return JsonResponse({"code": 400, "message": "invalid body"}, status=400)
    except Exception as e:
        return JsonResponse({"code": 500, "message": "error"}, status=500)


@require_http_methods(["POST"])
def logout(request):
    response = JsonResponse({"code": 200, "message": "ok"})
    response.delete_cookie("auth")
    return response


@require_http_methods(["GET"])
def get_favourite_spaces(request):
    userid = request.GET.get("id", "").strip()

    if not userid:
        return JsonResponse({"code": 400, "message": "missing fields"}, status=400)

    try:
        user = User.objects.get(id=userid)
    except User.DoesNotExist:
        return JsonResponse({"code": 404, "message": "invalid params"}, status=404)

    favourites = FavouriteSpace.objects.filter(user=user, status=0).values(
        "id", "space__id", "space__space_name", "create_time"
    )

    return JsonResponse({"code": 200, "message": "ok", "data": list(favourites)})


@require_http_methods(["GET"])
def get_booking_history(request):
    user_id = request.GET.get("id", "").strip()

    if not user_id:
        return JsonResponse({"code": 400, "message": "missing fields"}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"code": 404, "message": "invalid params"}, status=404)

    bookings = (
        Booking.objects.filter(user=user)
        .values(
            "id",
            "space__id",
            "space__space_name",
            "start_time",
            "end_time",
            "seat_no",
            "create_time",
        )
        .order_by("-start_time")
    )

    return JsonResponse({"code": 200, "message": "ok", "data": list(bookings)})


@require_http_methods(["POST"])
def submit_comment(request):
    """提交评论接口"""
    try:
        data = json.loads(request.body)
        email = data.get("email", "").strip()
        space_id = data.get("space_id", "")
        score = data.get("score", "")
        comment_description = data.get("comment", "").strip()

        # 1. 验证必填字段
        if not all([email, space_id, score, comment_description]):
            return JsonResponse(
                {"code": 400, "message": "缺失必填字段：邮箱、教室ID、评分、评论内容"},
                status=400,
            )

        # 2. 验证评分范围
        try:
            score = float(score)
            if not (1 <= score <= 5):
                raise ValueError
        except ValueError:
            return JsonResponse(
                {"code": 400, "message": "评分必须是1到5之间的数字"}, status=400
            )

        # 3. 查询用户和教室
        try:
            user = User.objects.get(email=email)
            space = LearningSpace.objects.get(id=space_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                {"code": 404, "message": "用户或教室不存在"}, status=404
            )

        # 4. 创建评论
        comment = Comment.objects.create(
            user=user,
            space=space,
            comment_description=comment_description,
            score=score,
            status=0,  # 默认状态为 Active
        )

        # 5. 返回成功响应
        return JsonResponse(
            {
                "code": 200,
                "message": "评论提交成功",
                "data": {
                    "comment_id": comment.id,
                    "user_email": user.email,
                    "space_id": space.id,
                    "score": comment.score,
                    "comment": comment.comment_description,
                    "create_time": comment.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                },
            }
        )

    except json.JSONDecodeError:
        return JsonResponse({"code": 400, "message": "无效的JSON格式"}, status=400)
    except Exception as e:
        return JsonResponse({"code": 500, "message": "error"}, status=500)


@require_http_methods(["GET"])
def get_comments(request):
    space_id = request.GET.get("space_id", "").strip()

    if not space_id:
        return JsonResponse({"code": 400, "message": "missing fields"}, status=400)

    comments = (
        Comment.objects.filter(space__id=space_id, status=0)
        .select_related("user")
        .order_by("-create_time")
        .values("id", "comment_description", "score", "create_time", "user__nickname")
    )

    comments_list = [
        {
            "id": c["id"],
            "comment": c["comment_description"],
            "score": c["score"],
            "created_time": c["create_time"],
            "nickname": c["user__nickname"],
        }
        for c in comments
    ]

    return JsonResponse(
        {
            "code": 200,
            "message": "查询成功",
            "data": comments_list,
        }
    )


@require_http_methods(["POST"])
def add_favourite_space(request):
    data = json.loads(request.body)
    user_id = data.get("userid")
    space_id = data.get("spaceid")
    if not user_id or not space_id:
        return JsonResponse({"code": 400, "message": "missing fields"}, status=400)

    FavouriteSpace.objects.get_or_create(
        user_id=user_id, space_id=space_id, defaults={"status": 0}
    )

    return JsonResponse({"code": 200, "message": "ok"})


@require_http_methods(["POST"])
def delete_favourite_space(request):
    data = json.loads(request.body)
    id = data.get("id")
    user_id = data.get("user_id")
    space_id = data.get("space_id")
    if not id and (not user_id or not space_id):
        return JsonResponse({"code": 400, "message": "missing fields"}, status=400)

    try:
        if id:
            favourite = FavouriteSpace.objects.get(id=id)
        else:
            favourite = FavouriteSpace.objects.get(user_id=user_id, space_id=space_id)
        favourite.delete()
        return JsonResponse({"code": 200, "message": "deleted successfully"})
    except FavouriteSpace.DoesNotExist:
        return JsonResponse({"code": 404, "message": "favourite not found"}, status=404)
