from django.urls import path
from .import views
from .views import return_chat_messages, get_rooms, chat_view

urlpatterns = [
    path('create/<username>/', return_chat_messages, name="return_chat_messages"),
    # path('get_rooms/<str:user1>/<str:user2>/', get_rooms, name="get_rooms"),
    path('get_rooms/<str:user1>/', get_rooms, name="get_rooms"),
    path('send_msg/<str:user1>/<str:user2>/', chat_view, name='chat_view')
]
