CREATE DATABASE jacd_swe_final;

-- TABLE CREATION
CREATE TABLE IF NOT EXISTS "user" (
    user_id         SERIAL,
    user_name       VARCHAR(255) NOT NULL,
    user_email      VARCHAR(255) NOT NULL,
    user_password   VARCHAR(255),
    user_first_name VARCHAR(255),
    user_last_name  VARCHAR(255),
    user_description    VARCHAR(1000),
    google_id       VARCHAR(255) UNIQUE,
    profile_picture   BYTEA,
    PRIMARY KEY (user_id)
);
CREATE TABLE IF NOT EXISTS "group" (
    group_id            SERIAL,
    user_id             SERIAL,
    group_name          VARCHAR(255) NOT NULL,
    group_description   VARCHAR(1000),
    group_public        BOOLEAN,
    group_picture       BYTEA,
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
    event_picture           BYTEA,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES "group"(group_id) ON DELETE CASCADE,
    PRIMARY KEY (event_id)
);

CREATE TABLE IF NOT EXISTS pending (
    user_id     SERIAL,
    event_id    SERIAL,
    attending   BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS membership (
    user_id     SERIAL,
    group_id    SERIAL,
    user_role   INT,
    joined      BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES "group"(group_id) ON DELETE CASCADE
);

-- END OF TABLE CREATION
-- TRIGGERS AND FUNCTIONS

-- END OF TRIGGERS AND FUNCTION
create or replace function update_on_membership()
returns trigger as
$update_on_membership$
begin
    insert into membership(user_id, group_id, user_role)
    values (NEW.user_id, NEW.group_id, 0);
    return NEW;
end;
$update_on_membership$
language plpgsql;

create or replace trigger update_membership
after insert
    on "group"
for each row execute
    function update_on_membership();
-- END OF TRIGGERS AND FUNCTIONS

-- INSERTIONS