from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    email = models.EmailField(max_length=255, unique=True, help_text='User email')
    password = models.CharField(max_length=255, help_text='Encrypted password')
    nickname = models.CharField(max_length=100, help_text='User nickname')
    create_time = models.DateTimeField(auto_now_add=True, help_text='Account creation time')

    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['email'], name='idx_email')
        ]

class LearningSpace(models.Model):
    STATUS_CHOICES = [
        (0, 'Open'),
        (1, 'Closed')
    ]

    space_name = models.CharField(max_length=255, help_text='Name')
    description = models.TextField(null=True, blank=True, help_text='Description')
    seat_num = models.IntegerField(help_text='Total number of seats')
    left_seat_num = models.IntegerField(help_text='Available seats count')
    left_seat_no_list = models.CharField(max_length=255, null=True, blank=True, help_text='Available seat list, e.g., [1,2,3]')
    score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, help_text='Average score')
    create_time = models.DateTimeField(auto_now_add=True, help_text='Creation time')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, help_text='Status: 0 - Open, 1 - Closed')

    class Meta:
        db_table = 'learning_space'
        indexes = [
            models.Index(fields=['status'], name='idx_status')
        ]

class Seat(models.Model):
    STATUS_CHOICES = [
        (0, 'Available'),
        (1, 'Reserved'),
        (2, 'Unavailable')
    ]

    space = models.ForeignKey(LearningSpace, on_delete=models.CASCADE, help_text='Associated learning space ID')
    seat_no = models.IntegerField(help_text='Seat number')
    status = models.IntegerField(choices=STATUS_CHOICES, help_text='Seat status')

    class Meta:
        db_table = 'seat'
        unique_together = ['space', 'seat_no']

class Comment(models.Model):
    STATUS_CHOICES = [
        (0, 'Active'),
        (1, 'Deleted'),
        (2, 'Maintenance report')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='User ID')
    space = models.ForeignKey(LearningSpace, on_delete=models.CASCADE, help_text='Learning space ID')
    comment_description = models.TextField(null=True, blank=True, help_text='Comment content')
    score = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating (1-5)'
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, help_text='Status')
    create_time = models.DateTimeField(auto_now_add=True, help_text='Creation time')
    update_time = models.DateTimeField(auto_now=True, help_text='Last update time')

    class Meta:
        db_table = 'comment'
        indexes = [
            models.Index(fields=['space'], name='idx_space')
        ]

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='User ID')
    space = models.ForeignKey(LearningSpace, on_delete=models.CASCADE, help_text='Learning space ID')
    start_time = models.DateTimeField(help_text='Start time')
    end_time = models.DateTimeField(help_text='End time')
    seat_no = models.IntegerField(help_text='Seat number')

    class Meta:
        db_table = 'booking'
        unique_together = ['space', 'seat_no', 'start_time']
        indexes = [
            models.Index(fields=['start_time', 'end_time'], name='idx_time_range')
        ]

class FavouriteSpace(models.Model):
    STATUS_CHOICES = [
        (0, 'Active'),
        (1, 'Removed')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='User ID')
    space = models.ForeignKey(LearningSpace, on_delete=models.CASCADE, help_text='Learning space ID')
    create_time = models.DateTimeField(auto_now_add=True, help_text='Favorite creation time')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, help_text='Status')

    class Meta:
        db_table = 'favourite_space'
        unique_together = ['user', 'space']

class ContactLog(models.Model):
    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Resolved')
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, help_text='User ID')
    email = models.EmailField(max_length=255, help_text='Contact email')
    message = models.TextField(help_text='Feedback content')
    create_time = models.DateTimeField(auto_now_add=True, help_text='Submission time')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, help_text='Processing status')

    class Meta:
        db_table = 'contact_log'
        indexes = [
            models.Index(fields=['status'], name='idx_process_status')
        ]