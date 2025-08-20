using TelemetryService;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHostedService<RabbitMqListener>();

var app = builder.Build();

app.MapGet("/", () => "TelemetryService is running.");

app.Run();
