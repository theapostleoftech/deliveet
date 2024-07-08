# in a new file, e.g., test_consumer.py
from channels.generic.websocket import WebsocketConsumer


class TestConsumer(WebsocketConsumer):
    def connect(self):
        print("Connection attempt")
        self.accept()

    def disconnect(self, close_code):
        print(f"Disconnected: {close_code}")

    def receive(self, text_data):
        print(f"Received: {text_data}")
        self.send(text_data="Hello from server!")
