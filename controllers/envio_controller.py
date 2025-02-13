import mysql.connector
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.envio_model import Envio
from fastapi.encoders import jsonable_encoder

class EnvioController:
    
    def create_envio(self, envio: Envio):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO envio (id_carga, id_empresa, id_transportador, fecha_asignacion)
                VALUES (%s, %s, %s, %s)
            """, (
                envio.id_carga,
                envio.id_empresa,
                envio.id_transportador,
                envio.fecha_asignacion
            ))

            conn.commit()
            return {"resultado": "Envío creado exitosamente"}
        
        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            if conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear el envío: {err}")
        
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def get_envio(self, envio_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM envio WHERE id = %s", (envio_id,))
            result = cursor.fetchone()
            
            if result:
                envio = {
                    'id': int(result[0]),
                    'id_carga': int(result[1]),
                    'id_empresa': int(result[2]),
                    'id_transportador': int(result[3]),
                    'fecha_asignacion': result[4]
                }
                return jsonable_encoder(envio)
            else:
                raise HTTPException(status_code=404, detail="Envío no encontrado")
        
        except mysql.connector.Error as err:
            if conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error en la base de datos: {err}")
        
        finally:
            if conn.is_connected():
                conn.close()

    def get_envios(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Consulta SQL actualizada para incluir el estado_actual de la carga
            cursor.execute("""
                SELECT e.id, e.id_carga, e.id_empresa, e.id_transportador,
                    u_transportador.nombre AS transportador_nombre, u_transportador.apellidos AS transportador_apellido,
                    u_empresa.nombre AS empresa_nombre, u_empresa.apellidos AS empresa_apellido,
                    c.estado_actual AS estado_carga  -- Agregamos el estado_actual de la carga
                FROM envio e
                LEFT JOIN usuario u_transportador ON e.id_transportador = u_transportador.id AND u_transportador.id_perfil = 2
                LEFT JOIN usuario u_empresa ON e.id_empresa = u_empresa.id AND u_empresa.id_perfil = 3
                LEFT JOIN carga c ON e.id_carga = c.id  -- Unimos la tabla carga para obtener el estado_actual
            """)
            result = cursor.fetchall()
            
            if not result:
                raise HTTPException(status_code=404, detail="Envíos no encontrados")
            
            envios = []
            for data in result:
                envio = {
                    'id': data[0],
                    'id_carga': int(data[1]),
                    'empresa': {
                        'nombre': data[6],  # Nombre de la empresa
                        'apellido': data[7]  # Apellido de la empresa
                    },
                    'transportador': {
                        'nombre': data[4],  # Nombre del transportador
                        'apellido': data[5]  # Apellido del transportador
                    },
                    'estado_carga': data[8]  # Estado actual de la carga
                }
                envios.append(envio)
            
            # Devolver el resultado dentro de un diccionario con la clave 'resultado'
            return jsonable_encoder({"resultado": envios})
        
        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            if conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al obtener los envíos: {err}")
        
        finally:
            if conn.is_connected():
                conn.close()





    def update_envio(self, envio_id: int, envio: Envio):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE envio 
                SET id_carga = %s, id_empresa = %s, id_transportador = %s, fecha_asignacion = %s 
                WHERE id = %s
            """, (
                envio.id_carga,
                envio.id_empresa,
                envio.id_transportador,
                envio.fecha_asignacion,
                envio_id
            ))

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Envío no encontrado")

            return {"resultado": "Envío actualizado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            if conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar el envío: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def delete_envio(self, envio_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM envio WHERE id = %s", (envio_id,))

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Envío no encontrado")

            return {"resultado": "Envío eliminado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            if conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar el envío: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

