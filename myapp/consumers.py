import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
logger = logging.getLogger(__name__)

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info('WebSocket connected')
        await self.accept()

    async def disconnect(self, close_code):
        logger.info('WebSocket disconnected')

    async def receive(self, text_data):
        logger.info('Message received')
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
     
        await self.send(text_data=json.dumps({'message': message }))
