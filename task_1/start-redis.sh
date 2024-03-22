#!/bin/bash

echo "Starting the Redis container..."
docker run --name redis-cache -d -p 6379:6379 redis
echo "Redis cache is up and running on port 6379."