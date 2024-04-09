CREATE DATABASE jacd_swe_final;

CREATE TABLE IF NOT EXISTS "user" (
    user_id         SERIAL,
    user_name       VARCHAR(255) NOT NULL,
    user_email      VARCHAR(255) NOT NULL,
    user_password   VARCHAR(255),
    user_first_name VARCHAR(255),
    user_last_name  VARCHAR(255),
    google_id       VARCHAR(255) UNIQUE,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS "group" (
    group_id            SERIAL,
    user_id             SERIAL,
    group_name          VARCHAR(255) NOT NULL,
    group_description   VARCHAR(1000),
    group_public        BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id),
    PRIMARY KEY (group_id)
);

CREATE TABLE IF NOT EXISTS event (
    event_id                SERIAL,
    user_id                 SERIAL,
    group_id                SERIAL,
    event_name              VARCHAR(255),
    event_description       VARCHAR(500),
    event_public            BOOLEAN,
    event_start_timestamp   TIMESTAMP,
    event_end_timestamp     TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id),
    FOREIGN KEY (group_id) REFERENCES "group"(group_id),
    PRIMARY KEY (event_id)
);

CREATE TABLE IF NOT EXISTS pending (
    user_id     SERIAL,
    event_id    SERIAL,
    attending   BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
);

CREATE TABLE IF NOT EXISTS membership (
    user_id     SERIAL,
    group_id    SERIAL,
    user_role   INT,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id),
    FOREIGN KEY (group_id) REFERENCES "group"(group_id)
);

CREATE TABLE IF NOT EXISTS collaboration (
    group_id    SERIAL,
    event_id    SERIAL,
    FOREIGN KEY (group_id) REFERENCES "group"(group_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
);

INSERT INTO "user" (user_name, user_password, user_email) VALUES
    ('Dom', 'dom123', 'dom@gmail.com'),
    ('Jason', 'jason123', 'jason@gmail.com'),
    ('Connor', 'connor123', 'connor@gmail.com'),
    ('Aidan', 'aidan', 'aidan@gmail.com');

INSERT INTO "group" (user_id, group_name, group_description, group_public) VALUES
    (1, 'ITCS 2181', 'COMPUTER SYSTEMS AHHHHH', TRUE),
    (2, 'ITCS 3155', 'SOFTWARE ENGINEERING AHHHHH', TRUE),
    (1, 'Bahamon Fan Club', 'a', FALSE);

INSERT INTO event (user_id, group_id, event_name, event_description, event_public, event_start_timestamp, event_end_timestamp) VALUES
    (1, 1, 'Birthday Bash', 'WOOO BIRTHDAY!!!', TRUE , '2024-06-23 00:00:00', '2024-06-24 00:00:00');

SELECT * FROM "user";

SELECT * FROM "group";

SELECT * FROM event;

SELECT event_id FROM event WHERE event_name = 'Birthday Bash';

SELECT group_id FROM "group" WHERE group_name = 'ITCS 2181';

DROP TABLE event CASCADE;

DROP DATABASE jacd_swe_final;