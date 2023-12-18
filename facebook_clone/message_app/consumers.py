from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from social_groups.exception import ClientError
from friend_app.models import FriendsList
from account.models import Accounts
from .constant import *
from .utils import calculate_timestamp, LazyRoomChatMessageEncoder
from django.utils import timezone
import asyncio
from django.core.paginator import Paginator
# from django.core.serializers import serialize
from account.utils import LazyAccountEncoder
import json
from .models import PrivateChatRoom, RoomChatMessage, UnreadChatRoomMessages


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection
        """
        print("PrivateChatConsumer: connect: " + str(self.scope['user']))
        await self.accept()

        self.room_id = None

    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        # Messages will have a "command" key we can switch on
        print("ChatConsumer: receive_json")
        command = content.get("command", None)
        try:
            if command == "join":
                await self.join_room(content["room"])
            elif command == "leave":
                await self.leave_room(content['room'])
            elif command == "send":
                if len(content["message"].lstrip()) != 0:
                    # raise ClientError(422,"You can't send an empty message.")
                    await self.send_room(content["room"], content["message"])
            elif command == "get_room_chat_messages":
                await self.display_progress_bar(True)
                room = await get_room_or_error(content['room_id'], self.scope["user"])
                payload = await get_room_chat_messages(room, content['page_number'])
                if payload != None:
                    payload = json.loads(payload)
                    await self.send_messages_payload(payload['messages'], payload['new_page_number'])
                else:
                    raise ClientError(
                        204, "Something went wrong retrieving the chatroom messages.")
                await self.display_progress_bar(False)
            elif command == "get_user_info":
                await self.display_progress_bar(True)
                room = await get_room_or_error(content['room_id'], self.scope['user'])
                payload = get_user_info(room, self.scope['user'])
                if payload != None:
                    payload = json.loads(payload)
                    await self.send_user_info_payload(payload['user_info'])
        except:
            pass

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave the room
        print("ChatConsumer: disconnect")
        try:
            if self.room_id != None:
                await self.leave_room(self.room_id)
        except Exception as e:
            print("EXCEPTION: " + str(e))
            pass

    async def join_room(self, room_id):
        """
        Called by receive_json when someone sent a join command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware (AuthMiddlewareStack)
        print("ChatConsumer: join_room: " + str(room_id))
        try:
            room = await get_room_or_error(room_id, self.scope['user'])
        except ClientError as e:
            return await self.handle_client_error(e)

        # Add user to "users" list for room
        await connect_user(room, self.scope["user"])

        # Store that we're in the room
        self.room_id = room.id

        await on_user_connected(room, self.scope["user"])

        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name
        )

        await self.send_json({
            "join": str(room.id)
        })

        if self.scope["user"].is_authenticated:
            # Notify the group that someone joined
            await self.channel_layer.group_send(
                room.group_name,
                {
                    "type": "chat.join",
                    "room_id": room_id,
                    "profile_image": self.scope["user"].profile_image.url,
                    "username": self.scope["user"].username,
                    "user_id": self.scope["user"].id,
                }
            )

    # These helper methods are named by the types we send - so chat.join becomes chat_join

    async def chat_join(self, event):
        """
        Called when someone has joined our chat.
        """
        # Send a message down to the client
        print("ChatConsumer: chat_join: " + str(self.scope["user"].id))
        if event["username"]:
            await self.send_json(
                {
                    "msg_type": MSG_TYPE_ENTER,
                    "room": event["room_id"],
                    "profile_image": event["profile_image"],
                    "username": event["username"],
                    "user_id": event["user_id"],
                    "message": event["username"] + " connected.",
                },
            )

    async def send_room(self, room_id, message):
        """
        Called by receive_json when someone sends a message to a room.
        """
        print("ChatConsumer: send_room")

        if self.room_id != None:
            if str(room_id) != str(self.room_id):
                raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")
        else:
            raise ClientError("ROOM_ACCESS_DENIED", "Room access denied")
        room = await get_room_or_error(room_id, self.scope['user'])

        connected_users = room.connected_users.all()

        # Execute these functions asychronously
        await asyncio.gather(*[
            append_unread_msg_if_not_connected(room, room.user1, connected_users, message),
            append_unread_msg_if_not_connected(room, room.user2, connected_users, message),
            create_room_chat_message(room, self.scope["user"], message)
        ])

        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.message",
                "profile_image": self.scope['user'].profile_image.url,
                "username": self.scope['user'].username,
                "user_id": self.scope['user'].id,
                "message": message
            }
        )

    async def chat_message(self, event):
        """
        Called when someone has messaged our chat.
        """
        # Send a message down to the client
        print("ChatConsumer: chat_message")

        timestamp = calculate_timestamp(timezone.now())

        await self.send_json({
            "msg_type": MSG_TYPE_MESSAGE,
            "username": event['username'],
            "user_id": event['user_id'],
            "profile_image": event['profile_image'],
            "message": event['message'],
            "natural_timestamp": timestamp,

        })

    async def display_progress_bar(self, is_displayed):
        """
        1. is_displayed = True
        - Display the progress bar on UI
        2. is_displayed = False
        - Hide the progress bar on UI
        """
        print("DISPLAY PROGRESS BAR: " + str(is_displayed))
        await self.send_json(
            {
                "display_progress_bar": is_displayed
            }
        )

    async def send_messages_payload(self, messages, new_page_number):
        """
        Send a payload of messages to the ui
        """
        print("ChatConsumer: send_messages_payload. ")
        await self.send_json(
            {
                "messages_payload": "messages_payload",
                "messages": messages,
                "new_page_number": new_page_number,
            },
        )

    async def send_user_info_payload(self, user_info):
        """
        Send a payload of user information to the ui
        """
        print("ChatConsumer: send_user_info_payload. ")
        await self.send_json({
            'user_info': user_info
        })

    async def leave_room(self, room_id):
        """
        Called by receive_json when someone sent a leave command.
        """
        # The logged-in user is in our scope thanks to the authentication ASGI middleware
        print("ChatConsumer: leave_room")
        room = await get_room_or_error(room_id, self.scope['user'])

        # Remove user from "connected_users" list
        await disconnect_user(room, self.scope["user"])

        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat.leave",
                "room_id": room_id,
                "profile_image": self.scope["user"].profile_image.url,
                "username": self.scope["user"].username,
                "user_id": self.scope["user"].id,
            }
        )

        # Remove that we're in the room
        self.room_id = None

        # Remove them from the group so they no longer get room messages
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name,
        )
        # Instruct their client to finish closing the room
        await self.send_json({
            "leave": str(room.id),
        })

    async def chat_leave(self, event):
        """
        Called when someone has left our chat.
        """
        # Send a message down to the client
        print("ChatConsumer: chat_leave")
        if event["username"]:
            await self.send_json(
                {
                    "msg_type": MSG_TYPE_LEAVE,
                    "room": event["room_id"],
                    "profile_image": event["profile_image"],
                    "username": event["username"],
                    "user_id": event["user_id"],
                    "message": event["username"] + " disconnected.",
                },
            )

    async def handle_client_error(self, e):
        """
        Called when a clienterror is raised.
        Sends error data to the UI
        """
        errorData = {}
        errorData['error'] = e.code
        if e.message:
            errorData['message'] = e.message
        return


@database_sync_to_async
def get_room_or_error(room_id, user):
    try:
        room = PrivateChatRoom.objects.get(pk=room_id)
    except PrivateChatRoom.DoesNotExist:
        raise ClientError("INVALID_ROOM", "Invalid Room.")

    if user != room.user1 and user != room.user2:
        raise ClientError("ROOM_ACCESS_DENIED",
                          "You do not have permission to join this room")

    friend_list = FriendsList.objects.get(user=user).friends.all()
    if not room.user1 in friend_list:
        if not room.user2 in friend_list:
            raise ClientError("ROOM_ACCESS_DENIED",
                              "You must be friends to chat")
    return room


@database_sync_to_async
def connect_user(room, user):
    # add user to connected_users list
    account = Accounts.objects.get(pk=user.id)
    return room.connect_user(account)


@database_sync_to_async
def disconnect_user(room, user):
    # remove from connected_users list
    account = Accounts.objects.get(pk=user.id)
    return room.disconnect_user(account)


@database_sync_to_async
def create_room_chat_message(room, user, message):
    return RoomChatMessage.objects.create(room=room, user=user, content=message)


@database_sync_to_async
def get_room_chat_messages(room, page_number):
    # time.sleep(1)
    try:
        qs = RoomChatMessage.objects.by_room(room)
        p = Paginator(qs, DEFAULT_ROOM_CHAT_MESSAGE_PAGE_SIZE)

        payload = {}
        # messages_data = None
        new_page_number = int(page_number)
        if new_page_number <= p.num_pages:
            new_page_number = new_page_number + 1
            s = LazyRoomChatMessageEncoder()
            payload['messages'] = s.serialize(p.page(page_number).object_list)
            # print(payload['messages'])
        else:
            payload['messages'] = "None"
        payload['new_page_number'] = new_page_number
        return json.dumps(payload)
    except Exception as e:
        print("EXCEPTION: " + str(e))
    return None

# @database_sync_to_async


def get_user_info(room, user):
    # time.sleep(1)
    try:
        other_user = room.user1
        if other_user == user:
            other_user = room.user2
        payload = {}
        s = LazyAccountEncoder()
        payload['user_info'] = s.serialize([other_user])[0]
        return json.dumps(payload)
    except ClientError as e:
        print("EXCEPTION: " + str(e))
    return None


# If the user is not connected to the chat, increment "unread messages" count
@database_sync_to_async
def append_unread_msg_if_not_connected(room, user, connected_users, message):
    if not user in connected_users:
        try:
            unread_msgs = UnreadChatRoomMessages.objects.get(
                room=room, user=user)
            unread_msgs.most_recent_message = message
            unread_msgs.count += 1
            unread_msgs.save()
        except UnreadChatRoomMessages.DoesNotExist:
            UnreadChatRoomMessages(room=room, user=user, count=1).save()
            pass
    return

# When a user connects, reset their unread message count to 0


@database_sync_to_async
def on_user_connected(room, user):
    # confirm they are in the connected users list
    connected_users = room.connected_users.all()
    if user in connected_users:
        try:
            # reset count
            unread_msgs = UnreadChatRoomMessages.objects.get(
                room=room, user=user)
            unread_msgs.count = 0
            unread_msgs.save()
        except UnreadChatRoomMessages.DoesNotExist:
            UnreadChatRoomMessages(room=room, user=user).save()
            pass
    return
