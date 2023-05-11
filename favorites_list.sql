CREATE TABLE favorites_list (
    username VARCHAR(255) NOT NULL,
    item_id INTEGER NOT NULL,
    PRIMARY KEY(username, item_id),
    FOREIGN KEY(item_id) REFERENCES item(item_id) ON DELETE CASCADE,
    FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE ON UPDATE CASCADE
);