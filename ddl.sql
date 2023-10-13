CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(50),
    password VARCHAR(255)
);

CREATE TABLE feedback(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(50),
    feedback TEXT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);