-- Initial database setup for PostgreSQL
-- This file is optional and runs on first container startup

-- Create UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create LTREE extension for hierarchical data
CREATE EXTENSION IF NOT EXISTS ltree;

-- Set connection limits
ALTER DATABASE ${DATABASE_NAME} CONNECTION LIMIT -1;
