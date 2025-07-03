# app/core/rabbitmq.py
import aio_pika
from app.core.config import RABBITMQ_URL

async def publish_sale_message(message: str):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("odoo_sales", durable=True)
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()), routing_key=queue.name
        )
