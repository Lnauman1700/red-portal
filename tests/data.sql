-- Mock Data For Tests

INSERT INTO users (email, password, role)
VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$nZcp3TLl$66257bad5279dfc1f1ce9cb6766ddb3bcb903a62d6836eff15c5b77fe2dfced0', 'teacher'),
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$rwsCyBeR$636bcf665edaf3595c5717a03d45fde31fe4a6cb4ad9476604a7991c98e9d59d', 'student');

INSERT INTO sessions (letter, session_time)
VALUES ('A', '2:00 - 4:20 MF'),
       ('B', '3:00-3:30 MTWHF');

INSERT INTO courses (teacher_id,course_number,course_name, course_info)
VALUES ('1', 'CSET 155', 'Database', 'Work with postgres SQL');
