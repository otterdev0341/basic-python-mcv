-- Create user and grant privileges
CREATE USER IF NOT EXISTS 'self_bank_user'@'%' IDENTIFIED BY 'self_bank_password';
GRANT ALL PRIVILEGES ON self_bank.* TO 'self_bank_user'@'%';
FLUSH PRIVILEGES; 