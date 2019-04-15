-- Mock Data For Tests

INSERT INTO users (email, password, role)
VALUES ('teacher@stevenscollege.edu', 'hwerty', 'teacher'),
       ('student@stevenscollege.edu', 'asdfgh', 'student');

INSERT INTO courses (teacher_id,course_number,course_name, course_info)
VALUES ('1', 'CSET 155', 'Database', 'Work with postgres SQL');

