import json
import math
from datetime import timedelta

from django.template.defaulttags import comment
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt

from learning_space.user.models import (
    LearningSpace,
    Booking,
    Comment,
    User,
    Seat,
    FavouriteSpace,
)


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great-circle distance between two points on Earth (in miles)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    r = 3958.8  # Earth's radius in miles
    return c * r


# def haversine_distance(lat1, lon1, lat2, lon2):
#     lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
#     R = 3958.8
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
#     return R * c


# 1. Retrieve classroom list endpoint (supports sorting by distance/rating)
def classroom_list(request):
    sort_by = request.GET.get("sort_by", "")
    # Get parameters from request
    lon_param = request.GET.get("longitude", None)
    lat_param = request.GET.get("latitude", None)

    try:
        user_lon = float(lon_param) if lon_param is not None else None
        user_lat = float(lat_param) if lat_param is not None else None
    except ValueError:
        user_lon, user_lat = None, None

    spaces = LearningSpace.objects.all()

    results = []
    for space in spaces:
        distance = None
        if (
            user_lon is not None
            and user_lat is not None
            and space.longitude is not None
            and space.latitude is not None
        ):
            distance = haversine(
                user_lon, user_lat, float(space.longitude), float(space.latitude)
            )
        comment_list = Comment.objects.filter(space_id=space.id)
        # mean score
        score = 0
        if comment_list:
            score = sum([b.score for b in comment_list]) / len(comment_list)
        else:
            score = float(space.score)
        results.append(
            {
                "id": space.id,
                "space_name": space.space_name,
                "description": space.description,
                "seat_num": space.seat_num,
                "left_seat_num": space.left_seat_num,
                "score": float(space.score) if score == 0 else score,
                "status": space.get_status_display(),  # 'Open' or 'Closed'
                "distance": distance,
                "latitude": float(space.latitude),
                "longitude": float(space.longitude),
            }
        )

    if sort_by == "distance" and user_lon is not None and user_lat is not None:
        results.sort(
            key=lambda x: x["distance"] if x["distance"] is not None else float("inf")
        )
    elif sort_by == "rating":
        results.sort(key=lambda x: x["score"], reverse=True)
    else:
        # Default sorting by rating in descending order
        results.sort(key=lambda x: x["score"], reverse=True)

    return JsonResponse(results, safe=False)


# 2. Retrieve detailed classroom information by classroom ID
def classroom_detail(request, classroom_id):
    user_id = request.GET.get("user_id")
    space = get_object_or_404(LearningSpace, pk=classroom_id)
    comment_list = Comment.objects.filter(space_id=classroom_id)
    # mean score
    score = 0
    if comment_list:
        score = sum([b.score for b in comment_list]) / len(comment_list)
    else:
        score = float(space.score)
    is_favourite = 0
    if user_id:
        is_favourite = FavouriteSpace.objects.filter(
            user_id=user_id, space_id=classroom_id
        ).exists()
        is_favourite = 1 if is_favourite else 0
    data = {
        "id": space.id,
        "space_name": space.space_name,
        "description": space.description,
        "seat_num": space.seat_num,
        "left_seat_num": space.left_seat_num,
        "score": float(space.score) if score == 0 else score,
        "longitude": float(space.longitude) if space.longitude is not None else None,
        "latitude": float(space.latitude) if space.latitude is not None else None,
        "status": space.get_status_display(),
        "create_time": space.create_time,
        "img_cover": space.img_cover,
        "is_favourite": is_favourite,
    }
    return JsonResponse(data)


# 3. Retrieve seat booking data by classroom ID
def classroom_booking_list(request, classroom_id):
    # Get classroom object
    space = get_object_or_404(LearningSpace, pk=classroom_id)

    # Generate full seat list: 1 to seat_num
    full_seat_list = list(range(1, space.seat_num + 1))

    now = timezone.now()

    active_bookings = Booking.objects.filter(
        space_id=classroom_id,
        create_time__gte=now - timedelta(days=1),
        end_time__gt=now,
    )
    # Collect seat numbers from booking records
    occupied_seats = set(b.seat_no for b in active_bookings)

    # Query all Seat records for this classroom, collecting seats under maintenance (status == 2)
    maintenance_seats = set()
    seat_objs = Seat.objects.filter(space=space)
    for seat in seat_objs:
        if seat.status == 2:
            maintenance_seats.add(seat.seat_no)

    # Construct seat status list: each object contains index and status
    seat_status_list = []
    for seat_no in full_seat_list:
        if seat_no in maintenance_seats:
            status = 2
        elif seat_no in occupied_seats:
            status = 1
        else:
            status = 0
        seat_status_list.append({"index": seat_no, "status": status})

    # Calculate current available seat count (status == 0)
    available_count = sum(1 for seat in seat_status_list if seat["status"] == 0)

    # Update left_seat_num field in LearningSpace table
    space.left_seat_num = available_count
    space.save(update_fields=["left_seat_num"])

    data = {
        "classroom_id": classroom_id,
        "seat_status_list": seat_status_list,
        "available_seat_count": available_count,
        "active_bookings": [
            {
                "seat_no": b.seat_no,
                "start_time": b.start_time,
                "end_time": b.end_time,
                "user_email": b.user.email if b.user else None,
            }
            for b in active_bookings
        ],
    }

    return JsonResponse(data)


# 4. Retrieve all ratings and review information for a classroom by classroom ID and user email
def classroom_review_list(request, classroom_id):
    email = request.GET.get("email", "")
    reviews = Comment.objects.filter(space_id=classroom_id)
    if email:
        reviews = reviews.filter(user__email=email).order_by("-create_time")
    review_data = []
    for r in reviews:
        review_data.append(
            {
                "id": r.id,
                "user_email": r.user.email,
                "comment_description": r.comment_description,
                "score": float(r.score),
                "status": r.get_status_display(),  # 'Active', 'Deleted', 'Maintenance report'
                "create_time": r.create_time,
                "update_time": r.update_time,
            }
        )
    data = {"classroom_id": classroom_id, "reviews": review_data}
    return JsonResponse(data)


@csrf_exempt
def get_booked_slots(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    space_id = request.GET.get("classroom_id")
    seat_no = request.GET.get("seat_no")
    date_str = request.GET.get("date")

    if not (space_id and seat_no and date_str):
        return JsonResponse(
            {"error": "Missing parameters: space_id, seat_no, and date are required."},
            status=400,
        )

    # 解析日期，格式要求为 YYYY-MM-DD
    try:
        date_obj = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse(
            {"error": "Invalid date format. Use YYYY-MM-DD."}, status=400
        )

    # 构造当天的起始和结束时间（使用 timezone.make_aware 保证时区正确）
    start_of_day = timezone.make_aware(
        timezone.datetime.combine(date_obj, timezone.datetime.min.time())
    )
    end_of_day = timezone.make_aware(
        timezone.datetime.combine(date_obj, timezone.datetime.max.time())
    )

    bookings = Booking.objects.filter(
        space_id=space_id,
        seat_no=seat_no,
        start_time__gte=start_of_day,
        end_time__lte=end_of_day,
    ).order_by("start_time")

    booked_slots = []
    for b in bookings:
        start_str = b.start_time.strftime("%H:%M")
        end_str = b.end_time.strftime("%H:%M")
        booked_slots.append(f"{start_str} - {end_str}")

    return JsonResponse({"booked_slots": booked_slots})


@csrf_exempt
def book_seat(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    required_fields = [
        "user_email",
        "classroom_id",
        "seat_no",
        "start_time",
        "end_time",
    ]
    if not all(field in data for field in required_fields):
        return JsonResponse({"error": "Missing required parameters"}, status=400)

    try:
        user = User.objects.get(email=data["user_email"])
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    # Parse booking time period
    start_time = parse_datetime(data["start_time"])
    end_time = parse_datetime(data["end_time"])
    if start_time is None or end_time is None:
        return JsonResponse({"error": "Invalid start_time or end_time"}, status=400)

    # check conflicting bookings
    conflicting_bookings = Booking.objects.filter(
        space_id=data["classroom_id"],
        seat_no=data["seat_no"],
        start_time__lt=end_time,
        end_time__gt=start_time,
    )
    if conflicting_bookings.exists():
        error_msg = (
            f"Time slot {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')} is unavailable."
            "\nCheck the unavailable time slots and choose a different one."
        )
        return JsonResponse({"message": error_msg}, status=400)

    # If no conflicts, create booking record
    booking = Booking.objects.create(
        user=user,
        space_id=data["classroom_id"],
        seat_no=data["seat_no"],
        start_time=start_time,
        end_time=end_time,
    )

    return JsonResponse(
        {"message": "Booking created successfully", "booking_id": booking.id}
    )


@csrf_exempt
def cancel_booking(request):
    if request.method != "POST":
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
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    required_fields = [
        "space_name",
        "seat_num",
        "left_seat_num",
        "score",
        "longitude",
        "latitude",
    ]
    if not all(field in data for field in required_fields):
        return JsonResponse({"error": "Missing required parameters"}, status=400)

    space = LearningSpace.objects.create(
        space_name=data["space_name"],
        description=data.get("description", ""),
        seat_num=data["seat_num"],
        left_seat_num=data["left_seat_num"],
        score=data["score"],
        longitude=data["longitude"],
        latitude=data["latitude"],
        status=data.get("status", 0),
        img_cover=data.get("img_cover", ""),
    )
    return JsonResponse(
        {
            "message": "Learning space created successfully",
            "learning_space_id": space.id,
        }
    )


@csrf_exempt
def update_learning_space(request, classroom_id):
    if request.method not in ["POST", "PUT"]:
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        space = LearningSpace.objects.get(pk=classroom_id)
    except LearningSpace.DoesNotExist:
        return JsonResponse({"error": "Learning space not found"}, status=404)

    # Update editable fields
    fields = [
        "space_name",
        "description",
        "seat_num",
        "left_seat_num",
        "score",
        "longitude",
        "latitude",
        "status",
        "img_cover",
    ]
    for field in fields:
        if field in data:
            setattr(space, field, data[field])
    space.save()
    return JsonResponse({"message": "Learning space updated successfully"})
