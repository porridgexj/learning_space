from django.test import TestCase, Client
from django.urls import reverse
from learning_space.user.models import User, LearningSpace, FavouriteSpace, Comment, Booking
import json
from learning_space.user.api_views import hash_password

class UserAPITestCase(TestCase):
    def setUp(self):
        """nitialize test users and learning spaces"""
        self.client = Client()
        self.test_email = "test@example.com"
        self.test_password = "securepass" # Original password
        self.test_nickname = "TestUser"
        
        # Create a test user (password hashing process)
        hashed_password = hash_password(self.test_password)
        self.user = User.objects.create(
            email=self.test_email, 
            password=hashed_password,  # Store the hashed password
            nickname=self.test_nickname
        )

        # Create a learning space
        self.space = LearningSpace.objects.create(space_name="Library", seat_num=50, left_seat_num=50)

    def test_register_user(self):
        """Test user registration"""
        response = self.client.post(
            reverse("register"),
            data=json.dumps({
                "email": "newuser@example.com",
                "password": "securepass",
                "nickname": "NewUser"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_id", response.json()["data"])

    def test_register_existing_user(self):
        """Test registration with an existing user"""
        response = self.client.post(
            reverse("register"),
            data=json.dumps({
                "email": self.test_email,
                "password": "securepass",
                "nickname": "NewUser"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_login_valid_user(self):
        """Test correct user login"""
        response = self.client.post(
            reverse("login"),
            data=json.dumps({
                "email": self.test_email,
                "password": self.test_password # Submit the original password, and the view will automatically hash it.
            }),
            
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("auth", response.cookies)  # Ensure the auth token is in cookies

    def test_login_invalid_password(self):
        """Test login with an incorrect password"""
        response = self.client.post(
            reverse("login"),
            data=json.dumps({
                "email": self.test_email,
                "password": "wrongpassword"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
    # Login firstly
     login_response = self.client.post(
        reverse("login"),
        data=json.dumps({
            "email": self.test_email,
            "password": self.test_password
        }),
        content_type="application/json"
    )
     self.client.cookies = login_response.cookies  # Save Cookie
    
    # Then logout
     response = self.client.post(reverse("logout"))
     self.assertEqual(response.status_code, 200)


    def test_add_favourite_space(self):
        """Test adding a learning space to the favorites list"""
        # Login firstly
        login_response = self.client.post(
            reverse("login"),
            data=json.dumps({
                "email": self.test_email,
                "password": self.test_password
            }),
            content_type="application/json"
        )
        self.client.cookies = login_response.cookies
        
        response = self.client.post(
            reverse("add_favourite_space"),  
            data=json.dumps({
                "userid": self.user.id,  
                "spaceid": self.space.id
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(FavouriteSpace.objects.filter(user=self.user, space=self.space).exists())

    def test_get_favourites(self):
        """Test retrieving the user's favorite learning spaces"""
        FavouriteSpace.objects.create(user=self.user, space=self.space)
        # Login firstly
        login_response = self.client.post(
            reverse("login"),
            data=json.dumps({
                "email": self.test_email,
                "password": self.test_password
            }),
            content_type="application/json"
        )
        self.client.cookies = login_response.cookies
        
        response = self.client.get(reverse("get_favourite_spaces"), {"id": self.user.id})  
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 1)

    def test_submit_comment(self):
        """Test submitting a review for a learning space"""
        # Login firstly
        login_response = self.client.post(
            reverse("login"),
            data=json.dumps({
                "email": self.test_email,
                "password": self.test_password
            }),
            content_type="application/json"
        )
        self.client.cookies = login_response.cookies
        
        response = self.client.post(
            reverse("submit_comment"),
            data=json.dumps({
                "email": self.test_email,
                "space_id": self.space.id,
                "score": 4,
                "comment": "Great space!"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(user=self.user, space=self.space).exists())

    def test_get_comments(self):
        """Test retrieving reviews of a learning space"""
    # Create a comment
        Comment.objects.create(
          user=self.user,
          space=self.space,
          comment_description="Great space!",
          score=5,
          status=0  
        )
    
    # Login
        login_response = self.client.post(
        reverse("login"),
        data=json.dumps({
            "email": self.test_email,
            "password": self.test_password
        }),
        content_type="application/json"
     )
        self.client.cookies = login_response.cookies
    
    # Then get the comment
        response = self.client.get(reverse("get_comments"), {"space_id": self.space.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 1)


    def test_get_booking_history(self):
        """Test retrieving the user's booking history"""
        Booking.objects.create(
            user=self.user,
            space=self.space,
            start_time="2024-04-01T10:00:00Z",
            end_time="2024-04-01T12:00:00Z",
            seat_no=1
        )
        # Login 
        login_response = self.client.post(
            reverse("login"),
            data=json.dumps({
                "email": self.test_email,
                "password": self.test_password
            }),
            content_type="application/json"
        )
        self.client.cookies = login_response.cookies
        
        response = self.client.get(reverse("get_booking_history"), {"id": self.user.id}) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 1)
