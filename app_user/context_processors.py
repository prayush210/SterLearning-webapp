from .models import Notification

def notification_list(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.all().filter(user=request.user)
    else:
        notifications = {}
    return {'notifications':notifications}
