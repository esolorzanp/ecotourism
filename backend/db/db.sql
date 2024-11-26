CREATE DATABASE dbEcoTourismEsp;

USE dbEcoTourismEsp;

CREATE TABLE perfiles(
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(200) NOT NULL
);

INSERT INTO
    perfiles (descripcion)
VALUES
    ('Administrador'),
    ('Empleado'),
    ('Supervisor');

CREATE TABLE usuarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(200) NOT NULL,
    correo VARCHAR(200) NOT NULL,
    clave VARCHAR(200) NOT NULL,
    id_perfil INT,
    CONSTRAINT FK_UsuariosPerfiles FOREIGN KEY (id_perfil) REFERENCES Perfiles(id)
);

CREATE TABLE sitios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(200) NOT NULL,
    detalle VARCHAR(2000) NOT NULL,
    urlImg VARCHAR(200) NOT NULL
);

CREATE TABLE galeria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(200) NOT NULL,
    orden SMALLINT NOT NULL,
    ruta VARCHAR(200) NOT NULL
);

CREATE TABLE comentarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(200) NOT NULL,
    ocupacion VARCHAR(200) NOT NULL,
    ciudadOrigen VARCHAR(200) NOT NULL,
    comentario VARCHAR(200) NOT NULL,
    calificacion TINYINT NOT NULL,
    fecha DATE NOT NULL
);

CREATE TABLE equipo(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    cargo VARCHAR(200) NOT NULL,
    edad SMALLINT NOT NULL,
    genero VARCHAR(200) NOT NULL,
    hobbies VARCHAR(200) NOT NULL,
    conocimientos VARCHAR(200),
    urlImg VARCHAR(200),
);

INSERT INTO
    equipo (
        nombre,
        cargo,
        edad,
        genero,
        hobbies,
        conocimientos
    )
VALUES
    (
        'Donald Trump',
        'CEO',
        '70',
        'Masculino',
        'Joder a Biden',
        'Empresario, presidente, administración'
    );

CREATE TABLE contactenos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(200) NOT NULL,
    correo VARCHAR(200) NOT NULL,
    comentarios VARCHAR(2000) NOT NULL
);

CREATE TABLE preguntasfrecuentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregunta VARCHAR(400) NOT NULL,
    respuesta VARCHAR(2000) NOT NULL,
    orden VARCHAR(200) NOT NULL
);