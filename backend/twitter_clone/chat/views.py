from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import PrivateChat, Message
from users.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q
from .serializers import MessageSerializer, PrivateRoomSerializer
from twitter_clone.pagination import CustomPagination
from notifications.models import Notification


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
def return_chat_messages(request, username):
    print('username is ', username)
    u2 = User.objects.get(username=username)
    # u1 = request.user
    # have to change this to get the username from post request
    u1 = User.objects.get(username='shovo456')
    print('u1 is ', u1)
    print('u2 is ', u2)
    room = PrivateChat.objects.using('male_user_db').filter(
        Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1)).first()
    messages = Message.objects.by_room(room)
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(messages, request)

    serializer = MessageSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'POST'])
def get_rooms(request, user1):
    u1 = User.objects.get(username=user1)
    # u2 = User.objects.get(username=user2)
    # u1 = request.user
    print('u1 is ', u1)
    print('request.data is ', request.method)

    if request.method == "GET":
        rooms = PrivateChat.objects.filter(Q(user1=u1) | Q(user2=u1))
        Notification.objects.filter(
            Q(notification_type='M',
              to_user=u1,
              )
        ).delete()
        # target_room = rooms.filter(Q(user1=u1, user2=u2)).first()
        # print(target_room)
        print("rooms")
    print("above post")
#     {
# "other_user":"shovo123",
# "latest_msg":" hello"
# }
    if request.method == "POST":
        print("inside post")
        other_user = request.data.get("other_user", None)
        # latest_msg = request.data.get("latest_msg", None)
        # print('latest_msg is ', latest_msg)
        print('other_user is ', other_user)
        rooms = PrivateChat.objects.filter(
            Q(user1__username__icontains=other_user, user2=u1) |
            Q(user1=u1, user2__username__icontains=other_user
              ))

    serializer = PrivateRoomSerializer(rooms, many=True)
    print('serializer.data is 1', serializer.data)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def chat_view(request, user1, user2):
    u1 = User.objects.get(username=user1)
    u2 = User.objects.get(username=user2)
    if request.method == "GET":
        # Handle GET request for retrieving messages and chat rooms
        u1 = User.objects.using('male_user_db').get(username=user1)
        rooms = PrivateChat.objects.filter(Q(user1=u1) | Q(user2=u1))
        Notification.objects.filter(
            Q(notification_type='M', to_user=u1)).delete()

        # Create a list to store serialized chat rooms with all messages
        chat_rooms_with_messages = []

        for room in rooms:
            # Retrieve all messages for the chat room
            messages = Message.objects.filter(room=room)

            # Serialize the chat room with all messages
            chat_room_data = PrivateRoomSerializer(room).data
            chat_room_data['messages'] = MessageSerializer(
                messages, many=True).data

            chat_rooms_with_messages.append(chat_room_data)

        return Response(chat_rooms_with_messages)
    # if request.method == "GET":
    #     # Handle GET request for retrieving messages and chat rooms
    #     u1 = User.objects.using('male_user_db').get(username='shovo456')
    #     rooms = PrivateChat.objects.filter(Q(user1=u1) | Q(user2=u1))
    #     Notification.objects.filter(
    #         Q(notification_type='M', to_user=u1)).delete()

    #     # Serialize and return chat rooms
    #     serializer = PrivateRoomSerializer(rooms, many=True)
    #     return Response(serializer.data)

    if request.method == "POST":
        print("running xx")
        # Handle POST request for sending a message
        u1 = User.objects.using('male_user_db').get(username='shovo123')
        u2 = User.objects.using('male_user_db').get(username='male')
        other_user = request.data.get("sender")
        text = request.data.get("text", None)
        print('other_user is ', other_user)
        print(u1.cover_pic)

        # Find or create a private chat room

        # room, created = PrivateChat.objects.get_or_create(
        #     Q(user1=u1, user2__username=other_user) & Q(
        #         user1__username=other_user, user2=u1)
        # )
        rooms = PrivateChat.objects.filter(Q(user1=u1) | Q(user2=u1))
        target_room = rooms.filter(
            Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1)).first()
        print(target_room)
        print("running asdf")
#         {
# "sender": "shovo123",
# "text": "hello2"

# }

        # Create a new message in the room
        message = Message(room=target_room, sender=u1, text=text)
        print(message)
        message.save(using='male_user_db')

        # Serialize and return the newly created message
        serializer = MessageSerializer(message)
        return Response(serializer.data)
