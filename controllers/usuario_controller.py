import mysql.connector
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.usuario_model import Usuario
from fastapi.encoders import jsonable_encoder

class UsuarioController:

    def create_usuario(self, usuario: Usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO usuario (usuario, contrasena, nombre, apellidos, documento, telefono, id_perfil, estado) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, 'activo')""",  # Asigna 'activo' por defecto
                           (usuario.usuario, usuario.contrasena, usuario.nombre, usuario.apellidos, 
                            usuario.documento, usuario.telefono, usuario.id_perfil))

            conn.commit()

            # **** CORRECCIÓN CLAVE: Obtener el ID del usuario recién insertado ****
            usuario_id = cursor.lastrowid  # Obtiene el ID autoincrementado

        # **** MODIFICACIÓN: Retornar el ID en la respuesta JSON ****
            return {"resultado": "Usuario creado exitosamente", "id": usuario_id}
            

        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            if conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear el usuario en la base de datos: {err}")

        except Exception as e:
            print(f"Error desconocido: {e}")
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def get_usuario(self, usuario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE id = %s", (usuario_id,))
            result = cursor.fetchone()

            if result is None:
                raise HTTPException(status_code=404, detail="User not found")

            content = {
                'id': int(result[0]),
                'usuario': result[1],
                'contrasena': result[2],
                'nombre': result[3],
                'apellidos': result[4],
                'documento': result[5],
                'telefono': result[6],
                'id_perfil': int(result[7]),
                'estado': result[8]  # Agrega el campo 'estado'
            }

            return jsonable_encoder(content)

        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            raise HTTPException(status_code=500, detail=f"Database error: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def get_usuarios(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario")
            result = cursor.fetchall()

            if not result:
                raise HTTPException(status_code=404, detail="No users found")

            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'usuario': data[1],
                    'contrasena': data[2],
                    'nombre': data[3],
                    'apellidos': data[4],
                    'documento': data[5],
                    'telefono': data[6],
                    'id_perfil': data[7],
                    'estado': data[8]  # Agrega el campo 'estado'
                }
                payload.append(content)

            return {"resultado": jsonable_encoder(payload)}

        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            raise HTTPException(status_code=500, detail=f"Database error: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def update_usuario(self, usuario_id: int, usuario: Usuario):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""UPDATE usuario 
                            SET usuario = %s, contrasena = %s, nombre = %s, apellidos = %s, 
                                documento = %s, telefono = %s, id_perfil = %s, estado = %s
                            WHERE id = %s""",
                        (usuario.usuario, usuario.contrasena, usuario.nombre, usuario.apellidos,
                            usuario.documento, usuario.telefono, usuario.id_perfil, usuario.estado, usuario_id))

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")

            return {"resultado": "Usuario actualizado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            if conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar el usuario en la base de datos: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def delete_usuario(self, usuario_id: int):
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Verificar si el usuario existe
            cursor.execute("SELECT * FROM usuario WHERE id = %s", (usuario_id,))
            usuario = cursor.fetchone()
            if usuario is None:
                raise HTTPException(status_code=404, detail="User not found")

            # Actualizar el estado del usuario a 'inactivo'
            cursor.execute("UPDATE usuario SET estado = 'inactivo' WHERE id = %s", (usuario_id,))
            conn.commit()

            return {"resultado": "Usuario inactivado exitosamente"}

        except mysql.connector.Error as err:
            if conn and conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al inactivar el usuario en la base de datos: {err}")

        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
