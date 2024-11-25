CREATE DATABASE dbEcoTourismEsp;

USE dbEcoTourismEsp;

CREATE TABLE Perfiles(
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(200) NOT NULL
);

INSERT INTO
    Perfiles (descripcion)
VALUES
    ('Administrador'),
    ('Empleado'),
    ('Supervisor');

CREATE TABLE Usuarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre varchar(200) NOT NULL,
    correo VARCHAR(200) NOT NULL,
    clave VARCHAR(200) NOT NULL,
    id_perfil INT,
    CONSTRAINT FK_UsuariosPerfiles FOREIGN KEY (id_perfil) REFERENCES Perfiles(id)
);

CREATE TABLE Sitios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(200) NOT NULL,
    detalle VARCHAR(200) NOT NULL,
    urlImg VARCHAR(200) NOT NULL
);

CREATE TABLE Galeria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(200) NOT NULL,
    orden SMALLINT NOT NULL,
    ruta VARCHAR(200) NOT NULL
);

CREATE TABLE Comentarios(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(200) NOT NULL,
    ocupacion VARCHAR(200) NOT NULL,
    ciudadOrigen VARCHAR(200) NOT NULL,
    comentario VARCHAR(200) NOT NULL,
    calificacion TINYINT NOT NULL,
    fecha DATE NOT NULL
);

CREATE TABLE Equipo(
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

CREATE TABLE Contactenos(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombres VARCHAR(200) NOT NULL,
    correo VARCHAR(200) NOT NULL,
    comentarios VARCHAR(2000) NOT NULL
);

CREATE TABLE PreguntasFrecuentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregunta VARCHAR(200) NOT NULL,
    respuesta VARCHAR(200) NOT NULL,
    orden VARCHAR(200) NOT NULL
);