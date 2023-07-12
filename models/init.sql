CREATE TABLE logins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO logins (username, password)
VALUES ('zayne', 'radia@betterearth');

INSERT INTO logins (username, password)
VALUES ('radia', 'radia@betterearth');

INSERT INTO logins (username, password)
VALUES ('trace', 'radia@betterearth');

INSERT INTO logins (username, password)
VALUES ('laura', 'radia@betterearth');
