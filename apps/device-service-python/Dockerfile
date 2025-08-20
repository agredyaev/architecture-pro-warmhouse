FROM python:3.9-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY proto/ ./proto/
RUN python -m grpc_tools.protoc \
    --proto_path=proto \
    --python_out=. \
    --grpc_python_out=. \
    proto/device/device.proto

COPY main.py .

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем сгенерированные файлы из правильной директории
COPY --from=builder /app/device/device_pb2.py ./device/
COPY --from=builder /app/device/device_pb2_grpc.py ./device/
COPY --from=builder /app/main.py .

CMD ["python", "main.py"]