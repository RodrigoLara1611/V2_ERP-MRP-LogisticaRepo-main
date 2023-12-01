CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    correo VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(255),
    fecha_registro DATETIME NOT NULL,
    perfil_img VARCHAR(255)
);

CREATE TABLE Vehiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    tipo VARCHAR(50) NOT NULL,
    modelo VARCHAR(255),
    capacidad VARCHAR(50) NOT NULL,
    imagen VARCHAR(255),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
);

CREATE TABLE Rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    origen VARCHAR(255) NOT NULL,
    destino VARCHAR(255) NOT NULL,
    fecha_recoleccion DATETIME NOT NULL,
    fecha_entrega DATETIME NOT NULL,
    vehiculo_id INT,
    estado VARCHAR(50) NOT NULL,
    FOREIGN KEY (vehiculo_id) REFERENCES Vehiculos(id)
);

CREATE TABLE SolicitudesEmbarque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    origen VARCHAR(255) NOT NULL,
    destino VARCHAR(255) NOT NULL,
    fecha_solicitud DATETIME NOT NULL,
    fecha_recoleccion_estimada DATETIME,
    fecha_entrega_estimada DATETIME,
    estado VARCHAR(50) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
);

CREATE TABLE Notificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    mensaje VARCHAR(500) NOT NULL,
    fecha_notificacion DATETIME NOT NULL,
    leido BOOLEAN NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
);

CREATE TABLE Reportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    fecha_reporte DATETIME NOT NULL,
    tipo VARCHAR(50) NOT NULL
);
