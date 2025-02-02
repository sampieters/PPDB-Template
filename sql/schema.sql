-- Create the Books table if it doesn't exist already
CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(80) NOT NULL
);

-- Insert some funny books for computer scientists
INSERT INTO books (title, author) VALUES
('The Linux Command Line', 'William Shotts'),
('The Mythical Man-Month', 'Frederick P. Brooks Jr.'),
('Press Reset', 'Jason Schreier'),
('How to code Snake in Python', 'Len Feremans'),
('Blood, Sweat, and Pixels', 'Jason Schreier');
