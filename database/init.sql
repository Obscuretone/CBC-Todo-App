-- Create the tasks table if it does not exist
CREATE TABLE IF NOT EXISTS tasks (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID()), 
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('pending', 'created', 'in_progress', 'completed') NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_uuid CHAR(36) NOT NULL -- Added user_uuid as CHAR(40) to relate tasks to users
);

-- Insert a sample task into the tasks table
INSERT INTO tasks (title, description) 
VALUES ('Sample Task', 'This is a sample task.');


-- Create the users table if it does not exist
CREATE TABLE IF NOT EXISTS users (
    uuid CHAR(36) PRIMARY KEY DEFAULT (UUID()), 
    display_name VARCHAR(255) NOT NULL,
    email VARCHAR(100),    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

