CREATE TABLE item(
    user_id INT,
    item_name VARCHAR(255),
    price FLOAT, 
    category VARCHAR(255),
    description VARCHAR(255),
    condition VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);