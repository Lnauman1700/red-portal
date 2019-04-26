-- Mock Data For Tests

INSERT INTO users (email, password, role)
VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$nZcp3TLl$66257bad5279dfc1f1ce9cb6766ddb3bcb903a62d6836eff15c5b77fe2dfced0', 'teacher'),
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$rwsCyBeR$636bcf665edaf3595c5717a03d45fde31fe4a6cb4ad9476604a7991c98e9d59d', 'student'),
       ('teacher2@stevenscollege.edu', 'pbkdf2:sha256:150000$qE6Fp30k$d2d0dbc4ebdcd6fc8ac2c7e656ecd80eff7fcc02a3d3402ddb4b58c97b48a2f5', 'teacher'),
       ('student_2@stevenscollege.edu', 'pbkdf2:sha256:150000$IVFJRywd$f7c324ac7fb5e8b1bb3dad19f9f029cb2c721e45a8c58949dba7e3627286363c', 'student');
       -- the password is x

INSERT INTO courses (teacher_id,course_number,course_name, course_info)
VALUES (1, 'CSET 155', 'Database', 'Work with postgres SQL'),
       (3, 'WET 000', 'Water', 'Waaaaaaater');

INSERT INTO sessions (letter, session_time, course_id)
VALUES ('A', '2:00 - 4:20 MF', 1),
       ('B', '3:00-3:30 MTWHF', 1),
       ('A', '6:00-8:00 MWF', 2);

INSERT INTO users_sessions (student, session)
VALUES (2, 2),
       (2, 3);
