using System.Text;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

namespace TelemetryService;

public class RabbitMqListener : BackgroundService
{
    private IConnection? _connection;
    private IModel? _channel;
    private readonly ILogger<RabbitMqListener> _logger;
    private readonly string _hostName;
    private readonly ConnectionFactory _factory;
   
    public RabbitMqListener(ILogger<RabbitMqListener> logger, IConfiguration configuration)
    {
    	_logger = logger;
    	_hostName = configuration["RabbitMqHost"] ?? "rabbitmq";
    	_factory = new ConnectionFactory() { HostName = _hostName, DispatchConsumersAsync = true, AutomaticRecoveryEnabled = true };
    }
   
    private void ConnectToRabbitMq(CancellationToken stoppingToken)
    {
    	var retryInterval = 5;
   
    	while (!stoppingToken.IsCancellationRequested)
    	{
    		try
    		{
    			_connection = _factory.CreateConnection();
    			_channel = _connection.CreateModel();
    			_logger.LogInformation("Successfully connected to RabbitMQ.");
    			return;
    		}
    		catch (RabbitMQ.Client.Exceptions.BrokerUnreachableException)
    		{
    			_logger.LogWarning($"Could not connect to RabbitMQ. Retrying in {retryInterval} seconds...");
    			Task.Delay(TimeSpan.FromSeconds(retryInterval), stoppingToken).Wait(stoppingToken);
    		}
    	}
    }
   
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
    	stoppingToken.Register(() => _logger.LogInformation("RabbitMqListener is stopping."));
   
    	await Task.Run(() =>
    	{
    		ConnectToRabbitMq(stoppingToken);
   
    		if (_channel != null && !stoppingToken.IsCancellationRequested)
    		{
    			_channel.ExchangeDeclare(exchange: "device_events", type: ExchangeType.Fanout);
    			
    			var queueName = _channel.QueueDeclare().QueueName;
    			_channel.QueueBind(queue: queueName,
    							  exchange: "device_events",
    							  routingKey: "");
   
    			var consumer = new AsyncEventingBasicConsumer(_channel);
    			consumer.Received += async (model, ea) =>
    			{
    				var body = ea.Body.ToArray();
    				var message = Encoding.UTF8.GetString(body);
    				try
    				{
    					_logger.LogInformation($"[x] Received {message}");
    					_channel.BasicAck(ea.DeliveryTag, false);
    				}
    				catch (Exception ex)
    				{
    					_logger.LogError(ex, $"Error processing message: {message}");
    					// Negative acknowledgement to requeue or discard the message.
    					_channel.BasicNack(ea.DeliveryTag, false, false); // false: don't requeue
    				}
    				await Task.CompletedTask;
    			};
    			
    			_channel.BasicConsume(queue: queueName,
    								 autoAck: false, // Switched to manual acknowledgment
    								 consumer: consumer);
    		}
    	}, stoppingToken);
    }
   
    public override void Dispose()
    {
    	_channel?.Close();
    	_connection?.Close();
    	base.Dispose();
    }
   }