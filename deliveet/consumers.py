"""
WebSocket Consumers for Real-time Features
- Delivery tracking
- Live notifications
- Location updates
"""
import json
import logging
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from urllib.parse import parse_qs
import jwt

logger = logging.getLogger(__name__)


class DeliveryTaskConsumer(WebsocketConsumer):
    """Consumer for delivery task updates"""
    
    def connect(self):
        self.delivery_task_id = self.scope['url_route']['kwargs']['delivery_task_id']
        self.delivery_task_group_name = f'delivery_task_{self.delivery_task_id}'

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
        try:
            text_data_json = json.loads(text_data)
            delivery_task = text_data_json.get('delivery_task', {})

            if delivery_task.get('courier_latitude') and delivery_task.get('courier_longitude'):
                if hasattr(self.scope['user'], 'courier_account'):
                    self.scope['user'].courier_account.courier_latitude = delivery_task['courier_latitude']
                    self.scope['user'].courier_account.courier_longitude = delivery_task['courier_longitude']
                    self.scope['user'].courier_account.save()

            # Send message to delivery_task group
            async_to_sync(self.channel_layer.group_send)(
                self.delivery_task_group_name,
                {
                    'type': 'delivery_task_update',
                    'delivery_task': delivery_task
                }
            )
        except Exception as e:
            logger.error(f"Error in delivery task consumer: {str(e)}")

    def delivery_task_update(self, event):
        delivery_task = event.get('delivery_task', {})
        self.send(text_data=json.dumps({
            'delivery_task': delivery_task
        }))


class DeliveryTrackerConsumer(AsyncWebsocketConsumer):
    """Async Consumer for real-time shipment tracking"""
    
    async def connect(self):
        self.shipment_id = self.scope['url_route']['kwargs']['shipment_id']
        self.user_token = self.scope['url_route']['kwargs']['user_token']
        self.room_name = f'shipment_tracker_{self.shipment_id}'
        self.room_group_name = f'tracker_{self.shipment_id}'

        # Validate token
        if not await self.validate_token(self.user_token):
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        logger.info(f"User connected to shipment tracker {self.shipment_id}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'location_update':
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'location_update',
                        'location': data.get('location')
                    }
                )
            elif message_type == 'status_update':
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'status_update',
                        'status': data.get('status')
                    }
                )
        except Exception as e:
            logger.error(f"Error in delivery tracker: {str(e)}")

    async def location_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'location_update',
            'location': event.get('location')
        }))

    async def status_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'status': event.get('status')
        }))

    async def validate_token(self, token):
        """Validate JWT token"""
        try:
            from django.conf import settings
            jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return True
        except:
            return False


class NotificationConsumer(AsyncWebsocketConsumer):
    """Async Consumer for real-time notifications"""
    
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_token = self.scope['url_route']['kwargs']['user_token']
        self.room_group_name = f'notifications_{self.user_id}'

        # Validate token
        if not await self.validate_token(self.user_token):
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        logger.info(f"User {self.user_id} connected to notifications")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            # Handle incoming notifications or acknowledgements
        except Exception as e:
            logger.error(f"Error in notification consumer: {str(e)}")

    async def send_notification(self, event):
        """Send notification to connected client"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'title': event.get('title'),
            'message': event.get('message'),
            'data': event.get('data')
        }))

    async def validate_token(self, token):
        """Validate JWT token"""
        try:
            from django.conf import settings
            jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return True
        except:
            return False
        }))
