-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS self_bank;

-- Create user if it doesn't exist
CREATE USER IF NOT EXISTS 'self_bank_user'@'%' IDENTIFIED BY 'self_bank_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON self_bank.* TO 'self_bank_user'@'%';

-- Flush privileges to apply changes
FLUSH PRIVILEGES; 