from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("signup", user_signup, name="signup-user"),
    path("auth-receiver", AuthGoogle.as_view(), name='auth-receiver'),
    path("change-username", change_username, name="change-username"),
    path("login", user_login, name="login"),
    path("logout", user_logout, name="logout"),
    path("settings", user_settings, name="settings"),
    path("tools", user_tools, name="tools"),
    path("send_friend_request/<int:user_id>/", send_friend_request, name="send-friend-request"),
    path("remove_friend/<int:user_id>/", remove_friend, name="remove-friend"),
    path("friends", user_friends, name="friends"),
    path("deny_friend_request/<int:user_id>/", deny_friend_request, name="deny-friend-request"),
    path("accept_friend_request/<int:user_id>/", accept_friend_request,
         name="accept-friend-request"),
    path("notification/<int:notification_id>/", notification, name="notification"),
    path("friend_suggestion/", friend_suggestion, name="friend-suggestion"),
    path("notification_socket", notification_socket, name="notification-socket"),
]
