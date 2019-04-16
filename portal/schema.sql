DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);

CREATE TABLE sessions (
    session_id bigserial PRIMARY KEY,
    letter varchar(1) NOT NULL,
    session_time varchar(100) NOT NULL
    --FOREIGN KEY course_id REFERENCES courses (course_id)
);
