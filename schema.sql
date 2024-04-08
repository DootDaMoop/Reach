CREATE TABLE IF NOT EXISTS "user" (
    user_id         SERIAL,
    user_name       VARCHAR(255) NOT NULL,
    user_password   VARCHAR(255) NOT NULL,
    user_email      VARCHAR(255) NOT NULL,
    user_first_name VARCHAR(255),
    user_last_name  VARCHAR(255),
    google_id       VARCHAR(255) UNIQUE,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS "group" (
    group_id    SERIAL,
    user_id     SERIAL,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id),
    PRIMARY KEY (group_id)
);

CREATE TABLE IF NOT EXISTS event (
    event_id    SERIAL,
    user_id     SERIAL,
    group_id    SERIAL,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id),
    FOREIGN KEY (group_id) REFERENCES "group"(group_id),
    PRIMARY KEY (event_id)
);

CREATE TABLE IF NOT EXISTS attending (
    user_id     SERIAL,
    event_id    SERIAL,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
);

CREATE TABLE IF NOT EXISTS membership (
    user_id     SERIAL,
    group_id    SERIAL,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id),
    FOREIGN KEY (group_id) REFERENCES "group"(group_id)
);

CREATE TABLE IF NOT EXISTS collaboration (
    group_id    SERIAL,
    event_id    SERIAL,
    FOREIGN KEY (group_id) REFERENCES "group"(group_id),
    FOREIGN KEY (event_id) REFERENCES event(group_id)
);

INSERT INTO "user" (user_name, user_password, user_email) VALUES
    ('Dom', 'dom123', 'dom@gmail.com'),
    ('Jason', 'jason123', 'jason@gmail.com'),
    ('Connor', 'connor123', 'connor@gmail.com'),
    ('Aidan', 'aidan', 'aidan@gmail.com');
