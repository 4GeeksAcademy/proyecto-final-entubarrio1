from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_migrate import migrate


db = SQLAlchemy()

class Vendedor(db.Model):
    __tablename__ = 'vendedor'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    productos = db.relationship('Producto', backref='vendedor', lazy=True)
    tiendas = db.relationship('Tienda', backref='vendedor', lazy=True)


    def __repr__(self):
        return f'<Vendedor {self.email}>'

    def serialize(self):
        tiendas = list(map(lambda item: item.serialize(), self.tiendas))
        return {
            "id": self.id,
            "email": self.email,
            "tiendas": True if len(tiendas) > 0  else False
            # do not serialize the password, its a security breach
        }
    
class Tienda(db.Model):
    __tablename__ = 'tienda'
    id = db.Column(db.Integer, primary_key=True)
    nombre_tienda = db.Column(db.String(120), unique=True, nullable=False)
    descripcion_tienda = db.Column(db.String(500), unique=False)
    categoria_tienda = db.Column(db.String(80), unique=False, nullable=False)
    direccion_tienda = db.Column(db.String(120), unique=False, nullable=False)
    url_imagen_tienda = db.Column(db.String(120), unique=False, nullable=False)
    productos = db.relationship('Producto', backref='tienda', lazy=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedor.id'))
    # particular_id = db.Column(db.Integer, db.ForeignKey('particular.id'))

    def __repr__(self):
        return f'<Tienda {self.nombre_tienda}>'

    def serialize(self):
        return {
            "id": self.id,
            "nombre_tienda": self.nombre_tienda,
            "descripcion_tienda": self.descripcion_tienda,   
            "categoria_tienda": self.categoria_tienda, 
            "direccion_tienda": self.direccion_tienda, 
            "url_imagen_tienda": self.url_imagen_tienda        
            # do not serialize the password, its a security breach
        }  
     
class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(120), unique=False, nullable=False)
    precio = db.Column(db.Integer, unique=False, nullable=False)
    descripcion_producto = db.Column(db.String(500), unique=False)
    categoria_producto = db.Column(db.String(80), unique=False, nullable=False)
    url_imagen_producto = db.Column(db.String(120), unique=False, nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedor.id'))
    tienda_id = db.Column(db.Integer, db.ForeignKey('tienda.id'))
    particular_id = db.Column(db.Integer, db.ForeignKey('particular.id'))

    # tienda = db.relationship('Tienda', backref='productos')

    def __repr__(self):
        return f'<Producto {self.nombre_producto}>'

    def serialize(self):
        result= Tienda.query.filter_by(id=self.tienda_id).first()
        return {
            "id": self.id,
            "nombre_producto": self.nombre_producto,
            "precio": self.precio,
            "nombre_tienda": result.serialize()["nombre_tienda"],
            "descripcion_producto": self.descripcion_producto,   
            "categoria_producto": self.categoria_producto, 
            "url_imagen_producto": self.url_imagen_producto,   
            "tienda_id": self.tienda_id        
            # do not serialize the password, its a security breach
        } 
    
class Particular(db.Model):
    __tablename__ = 'particular'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    # tienda_id = db.Column(db.Integer, db.ForeignKey('tienda.id'))
    productos = db.relationship('Producto', backref='particular', lazy=True)
    # tiendas = db.relationship('Tienda', backref='particular', lazy=True)
    # Otros campos que quieras agregar para usuarios particulares

    def __repr__(self):
        return f'<Particular {self.email}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
