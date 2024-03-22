@echo off
echo Starting RabbitMQ container...
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
echo RabbitMQ is starting up. Management UI will be available at http://localhost:15672
pause