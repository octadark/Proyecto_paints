from app_flask.config.mysqlconnection import connectToMySQL
from app_flask.modelos import modelo_usuarios
from flask import flash
from app_flask import BASE_DATOS

class Paint:
    def __init__(self, datos):
        self.id = datos['id']
        self.title = datos['title']
        self.description = datos['description']
        self.price = datos['price']
        self.fecha_creacion = datos['fecha_creacion']
        self.fecha_actualizacion = datos['fecha_actualizacion']
        self.id_usuario = datos['id_usuario']
        self.usuario = None

    @classmethod
    def crear_uno(cls, datos):
        query = """
                INSERT INTO paint (title, description, price, id_usuario)
                VALUES (%(title)s, %(description)s, %(price)s, %(id_usuario)s);
                """
        return connectToMySQL(BASE_DATOS).query_db(query, datos)

    @classmethod
    def obtener_todos(cls):
            query = """
                    SELECT * 
                    FROM paint JOIN usuarios
                    ON paint.id_usuario = usuarios.id;
                    """
            resultado = connectToMySQL(BASE_DATOS).query_db(query)
            lista_paint = []
            for renglon in resultado:
                paint_actual = cls(renglon)
                print(renglon)
                usuario = {
                    **renglon,
                    'nombre' : renglon['nombre'],
                    'id' : renglon['usuarios.id'],
                    'fecha_creacion' : renglon['fecha_creacion'],
                    'fecha_actualizacion' : renglon['fecha_actualizacion']
                }
                paint_actual.usuario = modelo_usuarios.Usuario(usuario)
                lista_paint.append(paint_actual)
            return lista_paint

    @classmethod
    def elimina_uno(cls, datos):
            query = """
                    DELETE FROM paint 
                    WHERE id = %(id)s;
                    """
            return connectToMySQL(BASE_DATOS).query_db(query, datos)
    
    @classmethod
    def actualizar_uno(cls, datos):
        query = """
                UPDATE paint 
                SET title = %(title)s, description = %(description)s, price = %(price)s,
                    id_usuario = %(id_usuario)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(BASE_DATOS).query_db(query, datos)
    
    @classmethod
    def obtener_uno(cls, datos):
        query = """
                SELECT *
                FROM paint
                WHERE id = %(id)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, datos)
        return cls(resultado[0])
    
    @classmethod
    def obtener_uno_con_usuario(cls, datos):
        query = """
                SELECT * 
                FROM paint JOIN usuarios
                    ON paint.id_usuario = usuarios.id
                WHERE paint.id = %(id)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, datos)
        renglon = resultado[0]
        paint = cls(renglon)
        usuario = {
            **renglon,
            "id" : renglon['usuarios.id'],
            "nombre" : renglon['nombre'],
            "fecha_creacion" : renglon['fecha_creacion'],
            "fecha_actualizacion" : renglon['fecha_actualizacion']
        }
        paint.usuario = modelo_usuarios.Usuario(usuario)
        return paint
    
    @staticmethod
    def validar_paint(datos):
        es_valido = True
        if len(datos['title']) < 2:
            flash('El nombre de la pintura debe tener al menos 2 caracteres', 'error_title')
            es_valido = False
        if len(datos['description']) < 10:
            flash('La descripción de la pintura debe tener al menos 10 caracteres.', 'error_description')
            es_valido = False
        if len(datos['price']) < 2:
            flash('Por favor agregale un precio a tu pintura.', 'error_price')
            es_valido = False
        return es_valido