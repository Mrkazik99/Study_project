-- Create the database if it does not exist
CREATE DATABASE IF NOT EXISTS service_database;

-- Create the user if it does not exist
CREATE USER IF NOT EXISTS 'service_user'@'%' IDENTIFIED BY '6EgF48arFnP7Ew';

-- Grant all privileges on the database to the user
GRANT ALL ON service_database.* TO 'service_user'@'%';