-- Mock Data For Tests

INSERT INTO users (email, password, role)
VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$nZcp3TLl$66257bad5279dfc1f1ce9cb6766ddb3bcb903a62d6836eff15c5b77fe2dfced0', 'teacher'),
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$rwsCyBeR$636bcf665edaf3595c5717a03d45fde31fe4a6cb4ad9476604a7991c98e9d59d', 'student');
