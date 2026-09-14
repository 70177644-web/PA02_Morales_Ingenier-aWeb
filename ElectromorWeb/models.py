from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from werkzeug.security import check_password_hash, generate_password_hash

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    empresa = Column(String)
    telefono = Column(String)
    correo = Column(String)

class Motor(Base):
    __tablename__ = "motores"
    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String)
    modelo = Column(String)
    potencia = Column(String)
    tipo = Column(String)
    serie = Column(String)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente")

class Orden(Base):
    __tablename__ = "ordenes"
    id = Column(Integer, primary_key=True, index=True)
    problema = Column(Text)
    fecha_ingreso = Column(DateTime)
    responsable = Column(String)
    motor_id = Column(Integer, ForeignKey("motores.id"))
    motor = relationship("Motor")

class Diagnostico(Base):
    __tablename__ = "diagnosticos"
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text)
    trabajos = Column(Text)
    repuestos = Column(Text)
    pruebas = Column(Text)
    observaciones = Column(Text)
    orden_id = Column(Integer, ForeignKey("ordenes.id"))
    orden = relationship("Orden")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
# Método para guardar contraseña encriptada
    def set_password(self, contraseña):
        self.password = generate_password_hash(contraseña)

    # Método para verificar contraseña
    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.password, contraseña)
class Reporte(Base):
    __tablename__ = "reportes"
    id = Column(Integer, primary_key=True, index=True)
    contenido = Column(Text)
    fecha = Column(DateTime)