CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    correo VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    fecha_registro DATETIME NOT NULL,
    perfil_img VARCHAR(255)
);

CREATE TABLE Vehiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    tipo VARCHAR(255) NOT NULL,
    modelo VARCHAR(255) NOT NULL,
    capacidad VARCHAR(255) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
);

CREATE TABLE Rutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    origen VARCHAR(255) NOT NULL,
    destino VARCHAR(255) NOT NULL,
    fecha_recoleccion DATETIME NOT NULL,
    fecha_entrega DATETIME NOT NULL,
    vehiculo_id INT,
    estado VARCHAR(255) NOT NULL,
    FOREIGN KEY (vehiculo_id) REFERENCES Vehiculos(id)
);

CREATE TABLE Productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    img_url VARCHAR(255) NOT NULL,
    cantidad_stock INT NOT NULL,
    precio_unitario FLOAT NOT NULL,
    estado VARCHAR(255) NOT NULL
);

CREATE TABLE OrdenesCompra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    usuario_id INT,
    cantidad INT NOT NULL,
    fecha_orden DATETIME NOT NULL,
    estado VARCHAR(255) NOT NULL,
    FOREIGN KEY (producto_id) REFERENCES Productos(id),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
);

CREATE TABLE Notificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    mensaje VARCHAR(255) NOT NULL,
    fecha_notificacion DATETIME NOT NULL,
    leido BOOLEAN NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id)
);

CREATE TABLE Reportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    fecha_reporte DATETIME NOT NULL,
    tipo VARCHAR(255) NOT NULL
);
