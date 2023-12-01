# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    correo = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    nombre = Column(String, index=True)
    fecha_registro = Column(DateTime, nullable=False)
    perfil_img = Column(String)
    # rela
    vehiculos = relationship("Vehiculo", back_populates="usuario")
    solicitudes_embarque = relationship("SolicitudEmbarque", back_populates="usuario")
    notificaciones = relationship("Notificacion", back_populates="usuario")

class Vehiculo(Base):
    __tablename__ = "vehiculos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    tipo = Column(String(50), nullable=False)
    modelo = Column(String)
    capacidad = Column(String(50), nullable=False)
    imagen = Column(String(255))
    # rela
    usuario = relationship("Usuario", back_populates="vehiculos")
    rutas = relationship("Ruta", back_populates="vehiculo")

class Ruta(Base):
    __tablename__ = "Rutas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    origen = Column(String(255), nullable=False)
    destino = Column(String(255), nullable=False)
    duracion_estimada = Column(String(50))  
    vehiculo_id = Column(Integer, ForeignKey('vehiculos.id'))
    # rela
    vehiculo = relationship("Vehiculo", back_populates="rutas")

class SolicitudEmbarque(Base):
    __tablename__ = "solicitudesembarque"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    origen = Column(String(255), nullable=False)
    destino = Column(String(255), nullable=False)
    fecha_solicitud = Column(DateTime, nullable=False)
    fecha_recoleccion_estimada = Column(DateTime)
    fecha_entrega_estimada = Column(DateTime)
    estado = Column(String(50), nullable=False)
    peso = Column(Numeric, nullable=False) 
    # rela
    usuario = relationship("Usuario", back_populates="solicitudes_embarque")

class Notificacion(Base):
    __tablename__ = "notificaciones"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    mensaje = Column(String(500), nullable=False)
    fecha_notificacion = Column(DateTime, nullable=False)
    leido = Column(Boolean, nullable=False)
    # rela
    usuario = relationship("Usuario", back_populates="notificaciones")

class Reporte(Base):
    __tablename__ = "reportes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    titulo = Column(String(255), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_reporte = Column(DateTime, nullable=False)
    tipo = Column(String(50), nullable=False)
