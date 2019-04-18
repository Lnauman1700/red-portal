DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);



CREATE TABLE courses(
	course_id bigserial PRIMARY KEY,
	teacher_id bigint REFERENCES users (id),
	course_number varchar(10) UNIQUE,
	--what about making sure that the user we reference is a teacher?
	course_name text NOT NULL,
	course_info text
)

--what if we have user data in users table which courses relies on, then what?