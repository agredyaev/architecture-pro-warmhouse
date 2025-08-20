import pytest
import grpc
from device import device_pb2
from device import device_pb2_grpc

@pytest.fixture(scope="module")
def grpc_channel():
    """Fixture to create a gRPC channel."""
    with grpc.insecure_channel('device-service:50051') as channel:
        yield channel

@pytest.fixture(scope="module")
def device_service_stub(grpc_channel):
    """Fixture to create a gRPC service stub."""
    return device_pb2_grpc.DeviceServiceStub(grpc_channel)

def test_add_and_get_device(device_service_stub):
    """Tests adding a new device and then retrieving it."""
    add_device_response = device_service_stub.AddDevice(device_pb2.AddDeviceRequest(
        type_id="thermostat-1",
        house_id="house-123",
        name="Living Room Thermostat",
        serial_number="SN-12345",
        config='{"temperature_unit": "C"}'
    ))
    device_id = add_device_response.device_id
    assert device_id is not None

    get_device_response = device_service_stub.GetDevice(device_pb2.GetDeviceRequest(device_id=device_id))
    assert get_device_response.device.id == device_id