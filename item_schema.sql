CREATE TABLE item(
    username INT NOT NULL,
    item_id SERIAL NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL, 
    category VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    condition VARCHAR(255) NOT NULL,
    PRIMARY KEY (item_id),
    FOREIGN KEY (username) REFERENCES users(username)
);