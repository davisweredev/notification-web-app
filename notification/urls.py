from django.urls import path
from . import views

urlpatterns = [
    path(
        '', 
        views.chat_page, 
        name='chat_page'
    ),
    path(
        'notifications/send/', 
        views.send_notification, 
        name='send_notification'
    ),
    path(
        'chat/', 
        views.chat_page, 
        name='chat'
    ),
   

]
