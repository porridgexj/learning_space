from django.urls import path, include
from . import api_views
from django.contrib import admin

urlpatterns = [
    # 1. Retrieve classroom list (supports sort_by=distance or sort_by=rating)
    path('api/v1/classrooms', api_views.classroom_list, name='classroom-list'),
    # 2. Retrieve detailed information of a classroom by classroom ID
    path('api/v1/classrooms/<int:classroom_id>', api_views.classroom_detail, name='classroom-detail'),
    # 3. Retrieve seat booking data for a classroom by classroom ID
    path('api/v1/classrooms/<int:classroom_id>/bookings', api_views.classroom_booking_list, name='classroom-bookings'),
    # 4. Retrieve all ratings and review information for a classroom by classroom ID and user email
    path('api/v1/classrooms/<int:classroom_id>/reviews', api_views.classroom_review_list, name='classroom-reviews'),
    # Book slot
    path('api/v1/classrooms/bookingslots', api_views.get_booked_slots, name='book-slot'),
    # Book a seat endpoint
    path('api/v1/bookings', api_views.book_seat, name='book-seat'),
    # Cancel a seat booking endpoint
    path('api/v1/bookings/cancel', api_views.cancel_booking, name='cancel-booking'),
    # Create a learning space endpoint
    path('api/v1/learning_spaces/create', api_views.create_learning_space, name='create-learning-space'),
    # Update learning space details endpoint
    path('api/v1/learning_spaces/<int:classroom_id>/update', api_views.update_learning_space, name='update-learning-space'),
]