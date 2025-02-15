import aio_pika
import asyncio
import yaml

from ace.settings import Settings
from ace.framework.resource import Resource


class DebugSettings(Settings):
    pass


class Debug(Resource):

    # TODO: Need this?
    def __init__(self):
        super().__init__()

    @property
    def settings(self):
        return DebugSettings(
            name="debug",
            label="Debug",
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    async def post_connect(self):
        await self.subscribe_debug_data()

    def post_start(self):
        asyncio.set_event_loop(self.bus_loop)
        self.bus_loop.create_task(self.update_layers_messages_state())

    async def debug_pre_disconnect(self):
        await self.unsubscribe_debug_data()

    async def publish_message(self, queue_name, message, delivery_mode=2):
        message = aio_pika.Message(
            body=message,
            delivery_mode=delivery_mode
        )
        await self.publisher_channel.default_exchange.publish(message, routing_key=queue_name)

    async def execute_resource_command(self, resource, command, kwargs=None):
        kwargs = kwargs or {}
        self.log.debug(f"[{self.labeled_name}] sending command '{command}' to resource: {resource}")
        queue_name = self.build_debug_queue_name(resource)
        message = self.build_message(resource, message={'method': command, 'kwargs': kwargs}, message_type='command')
        await self.publish_message(queue_name, message)

    async def update_layers_messages_state(self):
        for layer in self.settings.layers:
            await self.update_layer_messages_state(layer)

    async def update_layer_messages_state(self, layer):
        self.log.info(f"[{self.labeled_name}] sending debug_update_messages_state command to layer: {layer}")
        await self.execute_resource_command(layer, 'debug_update_messages_state')
        self.shutdown_complete = True

    async def message_data_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = message.body.decode()
        self.log.debug(f"[{self.labeled_name}] received a data message: {body}")
        try:
            data = yaml.safe_load(body)
        except yaml.YAMLError as e:
            self.log.error(f"[{self.labeled_name}] could not parse data message: {e}")
            return
        await self.post_debug_data(data)

    # TODO: need this method implemented.
    async def post_debug_data(self, data):
        self.log.info(f"{self.labeled_name} received debug data to POST: {data}")

    async def subscribe_debug_data(self):
        self.log.debug(f"{self.labeled_name} subscribing to debug data queue...")
        queue_name = self.settings.debug_data_queue
        self.consumers[queue_name] = await self.try_queue_subscribe(queue_name, self.message_data_handler)
        self.log.info(f"{self.labeled_name} Subscribed to debug data queue")

    async def unsubscribe_debug_data(self):
        queue_name = self.settings.debug_data_queue
        if queue_name in self.consumers:
            queue, consumer_tag = self.consumers[queue_name]
            self.log.debug(f"{self.labeled_name} unsubscribing from debug data queue...")
            await queue.cancel(consumer_tag)
            self.log.info(f"{self.labeled_name} Unsubscribed from debug data queue")
