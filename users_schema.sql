CREATE TABLE users (
    user_id SERIAL       NOT NULL,
    first_name    VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
<<<<<<< HEAD
    is_active BOOLEAN default false,
    PRIMARY KEY (user_id)
=======
    PRIMARY KEY (username)
>>>>>>> 19c1801fd5049c626a0e3140b75f6e22c20e6a36
);
