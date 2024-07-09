import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
logger = logging.getLogger(__name__)


class ShipmentOrderConsumer(WebsocketConsumer):

    def connect(self):
        logger.info(f"Attempting to connect: {self.scope['url_route']['kwargs']['delivery_task_id']}")
        self.delivery_task_id = self.scope['url_route']['kwargs']['delivery_task_id']
        self.delivery_task_group_name = 'delivery_task%s' % self.delivery_task_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.delivery_task_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.delivery_task_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        delivery_task = text_data_json['delivery_task']

        print("Delivery", delivery_task)

        if delivery_task.get('courier_latitude') and delivery_task.get('courier_longitude'):
            self.scope['user'].courier_account.courier_latitude = delivery_task['courier_latitude']
            self.scope['user'].courier_account.courier_longitude = delivery_task['courier_longitude']
            self.scope['user'].courier_account.save()

        # Send message to job group
        async_to_sync(self.channel_layer.group_send)(
            self.delivery_task_group_name,
            {
                'type': 'delivery_task_update',
                'delivery_task': delivery_task
            }
        )

    # Receive message from job group
    def delivery_task_update(self, event):
        delivery_task = event['delivery_task']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'delivery_task': delivery_task
        }))
