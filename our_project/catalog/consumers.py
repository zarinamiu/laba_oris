import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"pinkstore_chat_{self.room_name}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()

        user = self.scope.get("user")
        name = user.username if user and user.is_authenticated else "Аноним"

        self.send(text_data=json.dumps({
            "message": f"Система: Привет, {name}! Добро пожаловать в комнату {self.room_name}"
        }))

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"Система: Пользователь {name} подключился к комнате {self.room_name}",
            },
        )

    def disconnect(self, close_code):
        user = self.scope.get("user")
        name = user.username if user and user.is_authenticated else "Аноним"

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"Система: Пользователь {name} покинул комнату {self.room_name}",
            },
        )

    def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            self.send(text_data=json.dumps({
                "message": "Система: Ошибка формата сообщения"
            }))
            return

        message = data.get("message", "").strip()

        if not message:
            return

        user = self.scope.get("user")
        name = user.username if user and user.is_authenticated else "Анонимус"

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"{name}: {message}",
            },
        )

    def chat_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({
            "message": message
        }))