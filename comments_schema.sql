CREATE TABLE comments (
    username VARCHAR(255) NOT NULL,
    item_id INTEGER NOT NULL,
    comment VARCHAR(500) NOT NULL,
    comment_id SERIAL NOT NULL UNIQUE,
    PRIMARY KEY (comment_id),
    FOREIGN KEY(item_id) REFERENCES item(item_id) ON DELETE CASCADE,
    FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE
);