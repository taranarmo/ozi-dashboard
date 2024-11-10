-- Step 1: Create the database if it doesn't exist
CREATE DATABASE asn_stats;

-- Step 2: Switch to the 'asn_stats' database before proceeding.
\c asn_stats

-- Step 3: Create a user with secure privileges and a strong password
-- Make sure to replace 'change-this-one-before-running-the-query' with a secure password.
-- Please store the password securely and avoid hardcoding it in scripts and python code.
CREATE USER asn_stats WITH PASSWORD 'change-this-one-before-running-the-query';
GRANT ALL PRIVILEGES ON DATABASE asn_stats TO asn_stats;


