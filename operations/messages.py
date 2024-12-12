"""RabbitMQ opperations"""
from typing import Optional

import pika
import configuration
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection

rabbitmq_config = configuration.Config().rabbitmq


def get_connection() -> BlockingConnection:
    credentials = pika.PlainCredentials(username=rabbitmq_config.username, password=rabbitmq_config.password)
    return pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_config.host, rabbitmq_config.port, credentials=credentials))


def get_message_from_queue(channel: BlockingChannel, queue: str) -> Optional[str]:
    method_frame, header_frame, body = channel.basic_get(queue)
    if method_frame:
        channel.basic_ack(method_frame.delivery_tag)
        return body.decode('utf-8')
    return None
