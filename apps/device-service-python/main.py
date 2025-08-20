import grpc
import time
import json
import pika
from concurrent import futures
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from device import device_pb2
from device import device_pb2_grpc


class RabbitMQPublisher:
    def __init__(self, host):
        self.host = host
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        retry_interval = 5
        while self.connection is None:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
                self.channel = self.connection.channel()
                self.channel.exchange_declare(exchange='device_events', exchange_type='fanout')
                logging.info("Successfully connected to RabbitMQ.")
            except pika.exceptions.AMQPConnectionError:
                logging.warning(f"Could not connect to RabbitMQ. Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)

    def publish_message(self, message):
        try:
            self.channel.basic_publish(
                exchange='device_events',
                routing_key='',
                body=json.dumps(message)
            )
            logging.info(f" [x] Sent {message}")
        except pika.exceptions.AMQPError as e:
            logging.error(f"Failed to publish message: {e}. Attempting to reconnect...")
            self.connect() # Simple reconnect attempt

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()


class DeviceService(device_pb2_grpc.DeviceServiceServicer):
    def __init__(self, publisher):
        self.rabbitmq_publisher = publisher

    def AddDevice(self, request, context):
        logging.info(f"Received AddDevice request for device: {request.name}")

        # Simulate device ID creation
        device_id = f"fake-id-{request.serial_number}"

        # Prepare the event message for RabbitMQ
        event_message = {
            "event_type": "DeviceAdded",
            "device_id": device_id,
            "device_name": request.name,
            "type_id": request.type_id,
            "house_id": request.house_id
        }
        self.rabbitmq_publisher.publish_message(event_message)

        # Return the response as defined in the proto file
        return device_pb2.AddDeviceResponse(
            device_id=device_id
        )

    def GetDevice(self, request, context):
        logging.info(f"Received GetDevice request for device: {request.device_id}")

        # Simulate retrieving a device
        return device_pb2.GetDeviceResponse(
            device=device_pb2.Device(
                id=request.device_id,
                name="Living Room Thermostat",
                serial_number="SN-12345",
                type_id="thermostat-1",
                house_id="house-123",
                status="active"
            )
        )


def serve():
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
    publisher = RabbitMQPublisher(host=rabbitmq_host)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    device_pb2_grpc.add_DeviceServiceServicer_to_server(DeviceService(publisher), server)
    
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("DeviceService gRPC server started on port 50051.")
    
    def handle_shutdown(signum, frame):
        logging.info("Shutdown signal received. Stopping server...")
        publisher.close()
        server.stop(0)

    import signal
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        handle_shutdown(None, None)


if __name__ == '__main__':
    serve()