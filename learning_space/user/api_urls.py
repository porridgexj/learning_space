from django.urls import path
from . import api_views

urlpatterns = [
    path("register", api_views.register, name="register"),
    path("login", api_views.login, name="login_api"),
    path("logout", api_views.logout, name="logout"),
    path("favourites", api_views.get_favourite_spaces, name="get_favourite_spaces"),
    path("bookings", api_views.get_booking_history, name="get_booking_history"),
    path("comments", api_views.get_comments, name="get_comments"),
    path("comments/submit", api_views.submit_comment, name="submit_comment"),
    # path("add-favourite", api_views.add_favourite_space),
    path("add-favourite", api_views.add_favourite_space, name="add_favourite_space"),
    path("del-favourite", api_views.delete_favourite_space),
]
