import pytest
import pika
import json
import os

def test_send_telemetry():
    """Tests sending a telemetry message to RabbitMQ."""
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    channel.exchange_declare(exchange='telemetry_events', exchange_type='fanout')

    telemetry_message = {
        "device_id": "SN-12345",
        "timestamp": "2023-10-27T10:00:00Z",
        "temperature": 22.5,
        "humidity": 45.6
    }

    channel.basic_publish(
        exchange='telemetry_events',
        routing_key='',
        body=json.dumps(telemetry_message)
    )

    connection.close()