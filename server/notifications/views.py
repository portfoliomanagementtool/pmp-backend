from django.shortcuts import render
from .models import Notification
from .serializers import NotificationSerializer
from pmp_auth.decorators import auth_required

from django.http import JsonResponse
# Create your views here.

@auth_required
def get_notifications(request):
    try:
        notifications=Notification.objects.filter(user=request.pmp_user)
        serializer=NotificationSerializer(notifications,many=True)
        return JsonResponse({"data":serializer.data},safe=False)
    except Exception as e:

        return JsonResponse(status=400,data={"error":str(e)})
    
@auth_required
def mark_as_read(request):
    try:
        notification=Notification.objects.get(id=request.GET.get('id'))
        if notification.user!=request.pmp_user:
            return JsonResponse(status=400,data={"error":"You are not authorized to mark this notification as read"})
        notification.is_read=True
        notification.save()
        return JsonResponse({"message":"Notification marked as read"})
    except Exception as e:
        return JsonResponse(status=400,data={"error":str(e)})
    
@auth_required
def mark_as_read_all(request):
    try:
        notifications=Notification.objects.filter(user=request.pmp_user)
        for notification in notifications:
            notification.is_read=True
            notification.save()
        return JsonResponse({"message":"All notifications marked as read"})
    except Exception as e:
        return JsonResponse(status=400,data={"error":str(e)})

def create_notification(user,title,message):
    notification=Notification(user=user,title=title,message=message)
    notification.save()
    return notification