# Stage 1: Build the application
FROM golang:1.24-alpine AS builder
WORKDIR /app

# Cache dependencies
COPY go.mod ./
RUN go mod tidy
RUN go mod download

# Build the binary
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o temperature-api .

# Stage 2: Create the final, minimal image
FROM alpine:latest
WORKDIR /root/

# Copy the built binary from the builder stage
COPY --from=builder /app/temperature-api .

# Expose API port
EXPOSE 8081

# Run the application
CMD ["./temperature-api"]