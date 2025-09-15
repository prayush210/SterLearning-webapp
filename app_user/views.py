import random
import string
import os
from django.shortcuts import render, redirect, get_object_or_404
from google.oauth2 import id_token
from google.auth.transport import requests
from django.http import HttpResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib import messages
from app_quiz.models import Attempt
from .models import ExtendedUser, Friend, FriendRequest, Notification, Avatar, Decoration
from .forms import UserCreationWithEmailForm, GoogleUserChangeUsername, LoginForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return redirect('login')

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationWithEmailForm(request.POST)
        print(form['username'].value())
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationWithEmailForm()
    return render(request, 'register.html', {'form': form})

#https://www.photondesigner.com/articles/google-sign-in
@method_decorator(csrf_exempt, name='dispatch')
class AuthGoogle(APIView):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    def post(self, request, *args, **kwargs):
        try:
            user_data = self.get_google_user_data(request)
        except ValueError:
            return HttpResponse("Invalid Google token", status=403)

        user_email = user_data["email"]
        try:
            user = ExtendedUser.objects.get(
                email=user_email
            )
        except ObjectDoesNotExist:
            password = ''.join(random.choices(string.ascii_lowercase +
                                              string.ascii_uppercase + string.digits, k=20))
            user = ExtendedUser.objects.create(
                username=user_email,
                email=user_email,
                first_name=user_data["given_name"],
                password = password
                )
            login(request, user)
            return redirect('change-username')

        if user is not None:
            login(request, user)
        # Add any other logic, such as setting a http only auth cookie as needed here.
        return redirect('index')

    @staticmethod
    def get_google_user_data(request: HttpRequest):
        token = request.POST['credential']
        return id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )

@login_required
def change_username(request):
    if request.method == "POST":
        form = GoogleUserChangeUsername(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = GoogleUserChangeUsername(instance=request.user)
    return render(request, "change_username.html", {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

def user_settings(request):
    return render(request, 'settings.html')

def user_tools(request):
    return render(request, 'tools.html')

def add_friend(request, user_id):
    new_friend = ExtendedUser.objects.get(id=user_id)
    Friend.make_friend(request.user, new_friend)
    Friend.make_friend(new_friend, request.user)

def remove_friend(request, user_id):
    new_friend = ExtendedUser.objects.get(id=user_id)
    Friend.remove_friend(request.user, new_friend)
    Friend.remove_friend(new_friend, request.user)
    return redirect('friends')

def user_friends(request):
    if request.user.is_authenticated:
        users = ExtendedUser.objects.all()
        friends = {}
        sent_friend_requests = {}
        recieved_friend_requests = {}
        if request.user.is_authenticated:
            if Friend.objects.filter(current_user=request.user):
                friend = Friend.objects.get(current_user=request.user)
                friends = friend.users.all()
            if FriendRequest.objects.filter(sent_from=request.user):
                sent_friend_requests = FriendRequest.objects.all().filter(sent_from=request.user)
            if FriendRequest.objects.filter(sent_to=request.user):
                recieved_friend_requests = FriendRequest.objects.all().filter(sent_to=request.user)
        return render(request, 'friends.html', {'users':users, 'friends':friends,
                                                'sent_requests':sent_friend_requests, 
                                                'received_requests':recieved_friend_requests})
    else:
        return redirect('login')

def send_friend_request(request, user_id):
    new_friend = ExtendedUser.objects.get(id=user_id)
    friend_request = FriendRequest.objects.get_or_create(sent_from=request.user, sent_to=new_friend)
    current_notification = Notification.objects.get_or_create(message="Friend request: " +
                                                      request.user.username,
                                                      user=ExtendedUser.objects.get(id=user_id))
    return redirect('friends')

def remove_friend_request(request, user_id):
    new_friend = ExtendedUser.objects.get(id=user_id)
    friend_request = FriendRequest.objects.get(sent_from=new_friend, sent_to=request.user)
    friend_request.delete()

def deny_friend_request(request, user_id):
    remove_friend_request(request, user_id)
    return redirect('friends')

def accept_friend_request(request, user_id):
    add_friend(request, user_id)
    remove_friend_request(request, user_id)
    return redirect('friends')

def notification(request, notification_id):
    current_notification = Notification.objects.get(id=notification_id)
    current_notification.delete()
    return redirect('friends')

def friend_suggestion(request):
    quizzes = {}
    user_attempts = Attempt.objects.all().filter(user=request.user)
    for attempt in user_attempts:
        if attempt.completed:
            quizzes[attempt.quiz] = attempt.completed
    print(quizzes)
    quiz = random.choice(list(quizzes.keys()))
    other_attempts = Attempt.objects.all().filter(~Q(user=request.user))
    other_users = []
    for attempt in other_attempts:
        other_users.append(attempt.user)
    other_users = list(dict.fromkeys(other_users)) #remove duplicates
    if len(other_users) > 0:
        friend = random.choice(other_users)
        current_notification = Notification.objects.get_or_create(message="Friend Suggestion: " +
                                                          friend.username + " has completed the " +
                                                          quiz.name + " quiz too!",
                                                          user=request.user)
    return redirect('pathways-home')

def notification_socket(request):
    if request.method == "GET":
        current_notification = get_object_or_404(Notification, id = request.GET.get('notification'))
        current_notification.delete()
        return redirect('friends')

def shop(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            request_type = request.POST.get('type')
            request_id = request.POST.get('id')

            if request_type == 'buy_avatar':
                avatar = get_object_or_404(Avatar, id = request_id)

                if user.points() >= avatar.cost:
                    user.spentPoints += avatar.cost
                    user.inventoryAvatar.add(avatar)
                    user.save()

                    messages.add_message(request, messages.SUCCESS, 'You have successfully ' +
                                          'purchased ' + avatar.name + ' for ' + str(avatar.cost) + 
                                          ' points!')
                else:
                    messages.add_message(request, messages.ERROR, 'You do not have enough' +
                                           ' points for this item! Complete more quizzes to ' +
                                           'earn more points.')
            elif request_type == 'buy_decoration':
                decoration = get_object_or_404(Decoration, id = request_id)

                if user.points() >= decoration.cost:
                    user.spentPoints += decoration.cost
                    user.inventoryDecoration.add(decoration)
                    user.save()

                    messages.add_message(request, messages.SUCCESS, 'You have successfully ' +
                                          'purchased ' + decoration.name +
                                          ' for ' + str(decoration.cost) +
                                          ' points!')
                else:
                    messages.add_message(request, messages.ERROR, 'You do not have enough' +
                                           ' points for this item! Complete more quizzes to ' +
                                           'earn more points.')
            elif request_type == 'equip_avatar':
                avatar = get_object_or_404(Avatar, id = request_id)

                if user.inventoryAvatar.all().filter(id = request_id).count() == 1:
                    user.avatar = avatar
                    user.save()

                    messages.add_message(request, messages.SUCCESS, 'You have successfully ' +
                                          'equipped ' + avatar.name)
                else:
                    messages.add_message(request, messages.ERROR, 'You are unable to equip this.')
            elif request_type == 'equip_decoration':
                decoration = get_object_or_404(Decoration, id = request_id)

                if user.inventoryDecoration.all().filter(id = request_id).count() == 1:
                    user.decoration = decoration
                    user.save()

                    messages.add_message(request, messages.SUCCESS, 'You have successfully ' +
                                          'equipped ' + decoration.name)
                else:
                    messages.add_message(request, messages.ERROR, 'You are unable to equip this.')

        context = {}
        context['points'] = request.user.points
        context['equipped_avatar'] = request.user.avatar
        context['equipped_decoration'] = request.user.decoration
        context['owned_avatars'] = request.user.inventoryAvatar.all()
        context['owned_decorations'] = request.user.inventoryDecoration.all()
        context['avatars'] = Avatar.objects.exclude(id__in = context['owned_avatars'])
        context['decorations'] = Decoration.objects.exclude(id__in = context['owned_decorations'])

        return render(request, 'shop.html', context)
    else:
        messages.add_message(request, messages.ERROR, 'You need to be logged in')
        return redirect('login')
