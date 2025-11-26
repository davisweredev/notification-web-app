from django.shortcuts import render
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.db import models
from django.contrib.auth.models import User

@login_required
def chat_page(request):
    messages = Notification.objects.filter(
        models.Q(receiver=request.user) | models.Q(sender=request.user)
    ).order_by('created_at')[:50] 
    
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat.html', {
        'messages': messages, 
        'users': users
    })

@csrf_exempt
@login_required
def send_notification(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message")
            recipient_id = data.get("recipient_id")

            if not message or not recipient_id:
                return JsonResponse(
                    {"status": "error", "message": "Missing required fields"}, 
                    status=400
                )

            try:
                receiver = User.objects.get(id=recipient_id)
            except User.DoesNotExist:
                return JsonResponse(
                    {"status": "error", "message": "Recipient not found"}, 
                    status=404
                )

            notification = Notification.objects.create(
                message=message,
                sender=request.user,
                receiver=receiver
            )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"notifications_{receiver.id}",
                {
                    "type": "send_notification",
                    "message": notification.message,
                    "sender": request.user.username,
                    "id": notification.id,
                }
            )

            return JsonResponse({"status": "ok"})
            
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}, 
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {"status": "error", "message": str(e)}, 
                status=500
            )
    
    return JsonResponse(
        {"status": "error", "message": "Only POST method allowed"}, 
        status=400
        )