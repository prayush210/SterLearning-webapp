from django.contrib import auth
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django import forms
from app_quiz.models import Attempt, Quiz
from .context_processors import notification_list
from .forms import UserCreationWithEmailForm, GoogleUserChangeUsername, LoginForm
from .models import ExtendedUser, Decoration, Avatar, PointsAwarded, Friend, Notification, FriendRequest
from pathlib import Path
from django.test import TestCase
from django.core.files.images import ImageFile
from unittest.mock import patch
from django.contrib.auth import get_user_model

# Sample data located om sample_data folder
# Includes a placeholder image
ROOT_DIR = Path('sample_data')
IMAGE_PATH = 'Placeholder image.png'


class DecorationTests(TestCase):
    @classmethod
    # Create a valid Decoration
    def setUpTestData(cls):
        d1 = Decoration(name='TestDecoration1',
                        image=ImageFile(open(ROOT_DIR / IMAGE_PATH, 'rb'),
                                        name=IMAGE_PATH))
        d1.save()
        d1.full_clean()

    # Test database records creation of new Decoration
    def test_save_decoration(self):
        db_count = Decoration.objects.all().count()
        decoration = Decoration(name='NewDecoration',
                                image=ImageFile(open(ROOT_DIR / IMAGE_PATH, 'rb'),
                                        name=IMAGE_PATH))
        decoration.save()
        decoration.full_clean()
        self.assertEqual(db_count + 1, Decoration.objects.all().count())


class AvatarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        a1 = Avatar(name='TestAvatar1',
                    image=ImageFile(open(ROOT_DIR / IMAGE_PATH, 'rb'),
                                    name=IMAGE_PATH))
        a1.save()
        a1.full_clean()


def test_save_avatar(self):
    db_count = Avatar.objects.all().count()
    avatar = Avatar(name='NewAvatar',
                    image=ImageFile(open(ROOT_DIR / IMAGE_PATH, 'rb'),
                            name=IMAGE_PATH))
    avatar.save()
    avatar.full_clean()
    self.assertEqual(db_count+1, Avatar.objects.all().count())

class ExtendedUserTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        u1 = ExtendedUser(username='TestExtendedUser1',
                          password='TestPassword1',
                          email='testuser1@test.com')
        u1.save()
        u1.full_clean()

    # Test that a user can be saved with an avatar
    # and inventory avatar filled
    def test_avatar_user(self):
        a1 = Avatar(name='NewAvatar',
                    image=ImageFile(open(ROOT_DIR / IMAGE_PATH, 'rb'),
                                    name=IMAGE_PATH))
        a1.save()
        a1.full_clean()
        user = ExtendedUser(username='NewExtendedUser',
                            password='NewPassword',
                            email='newuser@test.com',
                            avatar=a1)
        user.save()
        user.full_clean()
        user.inventoryAvatar.add(a1)
        self.assertEqual(user.inventoryAvatar.all().count(),
                         1)

    # Test that a decoration can be saved to
    # a user and added to inventory
    def test_decoration_user(self):
        d1 = Decoration(name='NewDecoration',
                        image=ImageFile(open(ROOT_DIR / IMAGE_PATH, 'rb'),
                                        name=IMAGE_PATH))
        d1.save()
        d1.full_clean()
        user = ExtendedUser(username='NewExtendedUser',
                            password='NewPassword',
                            email='newuser@test.com',
                            decoration=d1)
        user.save()
        user.full_clean()
        user.inventoryDecoration.add(d1)
        self.assertEqual(user.inventoryDecoration.all().count(),
                         1)

# Test cases for the ExtendedUser model
class ExtendedUserModelTest(TestCase):

    # Test creating and retrieving a user
    def test_create_and_retrieve_user(self):
        ExtendedUser.objects.create(username='testuser', email='testuser@test.com')
        user = ExtendedUser.objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@test.com')


# Test cases for the PointsAwarded model
class PointsAwardedModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = ExtendedUser.objects.create(username='testuser', email='testuser@test.com')
        cls.points_awarded = PointsAwarded.objects.create(user=cls.user, points=10)

    # Test that points awarded carefully
    def test_points_awarded(self):
        self.assertEqual(self.points_awarded.user, self.user)
        self.assertEqual(self.points_awarded.points, 10)


# Test cases for templates
class TemplateTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    def test_change_username_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('change-username'))
        self.assertTemplateUsed(response, 'change_username.html')

    def test_friends_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('friends'))
        self.assertTemplateUsed(response, 'friends.html')

    def test_login_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'login.html')

    def test_register_template(self):
        response = self.client.get(reverse('signup-user'))
        self.assertTemplateUsed(response, 'register.html')

    def test_settings_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('settings'))
        self.assertTemplateUsed(response, 'settings.html')

    def test_shop_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('shop'))
        self.assertTemplateUsed(response, 'shop.html')


# Test cases for the Friend model
class FriendModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = ExtendedUser.objects.create(username='testuser1', email='testuser1@test.com')
        cls.user2 = ExtendedUser.objects.create(username='testuser2', email='testuser2@test.com')

    # Test the make_friend method
    def test_make_friend(self):
        Friend.make_friend(self.user1, self.user2)
        friend = Friend.objects.get(current_user=self.user1)
        self.assertIn(self.user2, friend.users.all())

    # Test the remove_friend method
    def test_remove_friend(self):
        Friend.make_friend(self.user1, self.user2)
        Friend.remove_friend(self.user1, self.user2)
        friend = Friend.objects.get(current_user=self.user1)
        self.assertNotIn(self.user2, friend.users.all())


# Test cases for the Notification model
class NotificationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = ExtendedUser.objects.create(username='testuser', email='testuser@test.com')

    # Test creating a notification
    def test_create_notification(self):
        Notification.objects.create(user=self.user, message='Test notification')
        notification = Notification.objects.get(user=self.user, message='Test notification')
        self.assertIsNotNone(notification)

    # Test marking a notification as read
    def test_mark_notification_as_read(self):
        notification = Notification.objects.create(user=self.user, message='Test notification')
        notification.is_read = True
        notification.save()
        self.assertTrue(Notification.objects.get(id=notification.id).is_read)

    # Test deleting a notification
    def test_delete_notification(self):
        notification = Notification.objects.create(user=self.user, message='Test notification')
        Notification.objects.get(id=notification.id).delete()
        with self.assertRaises(Notification.DoesNotExist):
            Notification.objects.get(id=notification.id)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('index')
        self.signup_url = reverse('signup-user')
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username='testuser', password='12345')

    # Test accessing the index page when authenticated
    def test_index_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 200)

    # Test accessing the index page when unauthenticated
    def test_index_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.index_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class UserSignupTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup-user')
        self.User = get_user_model()

    # Test valid form submission
    def test_valid_form_submission(self):
        user_count = self.User.objects.count()
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
        self.assertEqual(self.User.objects.count(), user_count + 1)

    # Test invalid form submission
    def test_invalid_form_submission(self):
        user_count = self.User.objects.count()
        response = self.client.post(self.signup_url, {
            'username': '',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.User.objects.count(), user_count)


class AuthGoogleTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.google_token = "valid_google_token"
        self.user_email = "test@example.com"
        self.user_given_name = "Test"

    # Test successful authentication with Google token
    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_auth_google_success(self, mock_verify_oauth2_token):
        mock_verify_oauth2_token.return_value = {
            "email": self.user_email,
            "given_name": self.user_given_name
        }

        response = self.client.post(reverse('auth-receiver'), {'credential': self.google_token})

        self.assertIsInstance(response, HttpResponseRedirect)

        redirect_url = response.url
        self.assertEqual(redirect_url, reverse('change-username'))

        self.assertTrue('_auth_user_id' in self.client.session)

        self.assertTrue(get_user_model().objects.filter(email=self.user_email).exists())

    # Test authentication failure with an invalid Google token
    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_auth_google_invalid_token(self, mock_verify_oauth2_token):
        mock_verify_oauth2_token.side_effect = ValueError

        response = self.client.post(reverse('auth-receiver'), {'credential': 'invalid_token'})

        self.assertEqual(response.status_code, 403)

    # Test when the user already exists in the database
    @patch('google.oauth2.id_token.verify_oauth2_token')
    def test_auth_google_user_exists(self, mock_verify_oauth2_token):
        get_user_model().objects.create_user(
            username=self.user_email,
            email=self.user_email,
            first_name=self.user_given_name
        )

        mock_verify_oauth2_token.return_value = {
            "email": self.user_email,
            "given_name": self.user_given_name
        }

        response = self.client.post(reverse('auth-receiver'), {'credential': self.google_token})

        self.assertIsInstance(response, HttpResponseRedirect)

        redirect_url = response.url
        self.assertEqual(redirect_url, reverse('index'))

        self.assertTrue('_auth_user_id' in self.client.session)


class ChangeUsernameTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(username='testuser', password='12345')
        self.change_username_url = reverse('change-username')

    # Test GET request to change username page
    def test_change_username_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.change_username_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_username.html')

    # Test POST request to change username
    def test_change_username_post(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.change_username_url, {'username': 'newusername'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('index'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')


class UserLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.test_user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    # Test login with correct username and password
    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('index'))

    # Test login with incorrect username or password
    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')


class UserLogoutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.test_user = self.user_model.objects.create_user(username='testuser', password='testpassword')

    # Test user logout
    def test_user_logout(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('logout'))

        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.assertRedirects(response, reverse('login'))


class UserSettingsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.test_user = self.user_model.objects.create_user(username='testuser', password='testpassword')

    # Test user settings
    def test_user_settings(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('settings'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'settings.html')


class RemoveFriendTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='pass')
        self.user2 = self.user_model.objects.create_user(username='user2', password='pass')
        Friend.make_friend(self.user1, self.user2)
        Friend.make_friend(self.user2, self.user1)

    # Test removing a friend
    def test_remove_friend(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('remove-friend', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Friend.objects.filter(current_user=self.user1, users__in=[self.user2]).exists())
        self.assertFalse(Friend.objects.filter(current_user=self.user2, users__in=[self.user1]).exists())


class UserFriendsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='pass')
        self.user2 = self.user_model.objects.create_user(username='user2', password='pass')
        Friend.make_friend(self.user1, self.user2)
        Friend.make_friend(self.user2, self.user1)

    # Test user friend functionality
    def test_user_friends(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('friends'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friends.html')
        self.assertIn('users', response.context)
        self.assertIn('friends', response.context)
        self.assertIn('sent_requests', response.context)
        self.assertIn('received_requests', response.context)
        self.assertIn(self.user2, response.context['friends'])


class FriendRequestTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='pass')
        self.user2 = self.user_model.objects.create_user(username='user2', password='pass')

    # Test sending a friend request
    def test_send_friend_request(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('send-friend-request', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful request
        self.assertTrue(FriendRequest.objects.filter(sent_from=self.user1, sent_to=self.user2).exists())

    # Test denying a friend request
    def test_deny_friend_request(self):
        FriendRequest.objects.create(sent_from=self.user1, sent_to=self.user2)
        self.client.login(username='user2', password='pass')
        response = self.client.get(reverse('deny-friend-request', args=[self.user1.pk]))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful denial
        self.assertFalse(FriendRequest.objects.filter(sent_from=self.user1, sent_to=self.user2).exists())

    # Test accepting a friend request
    def test_accept_friend_request(self):
        FriendRequest.objects.create(sent_from=self.user1, sent_to=self.user2)
        self.client.login(username='user2', password='pass')
        response = self.client.get(reverse('accept-friend-request', args=[self.user1.pk]))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful acceptance
        self.assertFalse(FriendRequest.objects.filter(sent_from=self.user1, sent_to=self.user2).exists())
        self.assertTrue(Friend.objects.filter(current_user=self.user1, users__in=[self.user2]).exists())
        self.assertTrue(Friend.objects.filter(current_user=self.user2, users__in=[self.user1]).exists())


class NotificationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='pass')
        self.notification = Notification.objects.create(user=self.user1, message='Test notification')

    # Test notification view
    def test_notification_view(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('notification', args=[self.notification.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Notification.objects.filter(
            pk=self.notification.pk).exists())


class FriendSuggestionViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.user1 = self.user_model.objects.create_user(username='user1', password='pass')
        self.user2 = self.user_model.objects.create_user(username='user2', password='pass')
        self.quiz = Quiz.objects.create(name='Test Quiz')
        Attempt.objects.create(user=self.user1, quiz=self.quiz, completed=True)
        Attempt.objects.create(user=self.user2, quiz=self.quiz, completed=True)

    # Test friend suggestion view
    def test_friend_suggestion_view(self):
        self.client.login(username='user1', password='pass')
        response = self.client.get(reverse('friend-suggestion'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Notification.objects.filter(
            user=self.user1).exists())
        notification = Notification.objects.get(user=self.user1)
        self.assertIn('Friend Suggestion:',
                      notification.message)
        self.assertIn('has completed the Test Quiz quiz too!', notification.message)


class NotificationSocketViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.test_user = self.user_model.objects.create_user(username='testuser', password='testpassword')
        self.notification = Notification.objects.create(user=self.test_user, message='Test notification')
        self.notification_socket_url = reverse('notification-socket')

    # Test notification socket functionality
    def test_notification_socket(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.notification_socket_url, {'notification': self.notification.id})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('friends'))
        self.assertFalse(Notification.objects.filter(id=self.notification.id).exists())


class UserCreationWithEmailFormTest(TestCase):

    # Test form field labels
    def test_form_field_labels(self):
        form = UserCreationWithEmailForm()
        self.assertEqual(form.fields['username'].label, 'Username')
        self.assertEqual(form.fields['email'].label, 'Email')

    # Test form field widget types
    def test_form_field_widget_type(self):
        form = UserCreationWithEmailForm()
        self.assertIsInstance(form.fields['username'].widget, forms.TextInput)
        self.assertIsInstance(form.fields['email'].widget, forms.EmailInput)

    # Test form with valid data
    def test_form_valid_data(self):
        form = UserCreationWithEmailForm({
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertTrue(form.is_valid())

    # Test form with invalid data
    def test_form_invalid_data(self):
        form = UserCreationWithEmailForm({
            'username': '',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertFalse(form.is_valid())


class GoogleUserChangeUsernameFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')

    # Test form with valid data
    def test_form_valid_data(self):
        form = GoogleUserChangeUsername(data={'username': 'newusername'}, instance=self.user)
        self.assertTrue(form.is_valid())

    # Test form with invalid data
    def test_form_invalid_data(self):
        form = GoogleUserChangeUsername(data={'username': ''}, instance=self.user)
        self.assertFalse(form.is_valid())


class LoginFormTest(TestCase):

    # Test form with valid data
    def test_form_valid_data(self):
        form = LoginForm(data={'username': 'testuser', 'password': 'testpassword'})
        self.assertTrue(form.is_valid())

    # Test form with invalid data
    def test_form_invalid_data(self):
        form = LoginForm(data={'username': '', 'password': 'testpassword'})
        self.assertFalse(form.is_valid())


class NotificationListTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = ExtendedUser.objects.create_user(username='testuser', password='testpassword')
        self.notification = Notification.objects.create(user=self.user, message='Test notification')

    # Test notification list for authenticated user
    def test_notification_list_authenticated(self):
        request = self.factory.get('/')
        request.user = self.user
        result = notification_list(request)
        self.assertEqual(len(result['notifications']), 1)
        self.assertEqual(result['notifications'][0], self.notification)

    # Test notification list for unauthenticated user
    def test_notification_list_unauthenticated(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()
        result = notification_list(request)
        self.assertEqual(result['notifications'], {})
