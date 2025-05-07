#!/bin/bash

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if mysqladmin ping -h"mysql" -u"root" -p"rootpassword" --silent; then
        echo "MySQL is ready!"
        break
    fi
    echo "Attempt $attempt of $max_attempts: MySQL is not ready yet..."
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    echo "Error: MySQL did not become ready in time"
    exit 1
fi

# Execute the initialization script
echo "Executing initialization script..."
if mysql -h"mysql" -u"root" -p"rootpassword" < /docker-entrypoint-initdb.d/init.sql; then
    echo "Initialization completed successfully!"
else
    echo "Error: Failed to execute initialization script"
    exit 1
fi 