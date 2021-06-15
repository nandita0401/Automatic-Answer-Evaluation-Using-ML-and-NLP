DROP TABLE IF EXISTS adminn;

CREATE TABLE adminn (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    fname TEXT NOT NULL,
    email VARCHAR NOT NULL,
    question VARCHAR NOT NULL,
    keywords TEXT NOT NULL, 
    mark_obtained INT NOT NULL
    );