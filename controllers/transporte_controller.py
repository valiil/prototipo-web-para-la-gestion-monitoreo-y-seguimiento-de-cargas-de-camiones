import mysql.connector
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.transporte_model import Transporte
from fastapi.encoders import jsonable_encoder

class TransporteController:
        
    def create_transporte(self, transporte: Transporte):   
        try:
            # Establecer la conexión con la base de datos
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insertar el nuevo transporte en la base de datos
            cursor.execute("""
                INSERT INTO transporte (matricula, modelo, tipo, color, capacidad, alto, ancho, largo, ano, id_perfil) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                transporte.matricula,
                transporte.modelo,
                transporte.tipo,
                transporte.color,
                transporte.capacidad,
                transporte.alto,
                transporte.ancho,
                transporte.largo,
                transporte.ano,
                transporte.id_perfil
            ))

            # Confirmar la transacción
            conn.commit()
            
            # Devolver un mensaje de éxito
            return {"resultado": "Transporte creado exitosamente"}

        except mysql.connector.Error as err:
            # Imprimir el error en la consola para depurar
            print(f"Error en la base de datos: {err}")
            
            # Si la conexión está activa, hacer rollback de la transacción
            if conn.is_connected():
                conn.rollback()
            
            # Lanzar una excepción HTTP con detalles del error
            raise HTTPException(status_code=500, detail=f"Error al crear el transporte en la base de datos: {err}")

        except Exception as e:
            # Captura cualquier otra excepción no manejada y lanza un error 500 con el mensaje del error
            print(f"Error desconocido: {e}")
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

        finally:
            # Asegurarse de cerrar la conexión si está activa
            if conn.is_connected():
                cursor.close()
                conn.close()

    def get_transporte(self, transporte_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transporte WHERE id = %s", (transporte_id,))
            result = cursor.fetchone()
            payload = [] 
            content = {} 
            
            content={
                    'id':int(result[0]),
                    'matricula':(result[1]),
                    'modelo':result[2],
                    'tipo':result[3],
                    'color':result[4],
                    'capacidad':result[5],
                    'alto':result[6],
                    'ancho':result[7],
                    'largo':result[8],
                    'ano':result[9],
                    'id_perfil':int(result[10])    
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
                return json_data
            else:
                raise HTTPException(status_code=404, detail="Transporte no encontrado")  
                
        except mysql.connector.Error as err:
            conn.rollback()
        finally:
            conn.close()

    def get_transportes(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transporte")
            result = cursor.fetchall()
            
            if not result:
                raise HTTPException(status_code=404, detail="Transportes no encontrados")
            
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'matricula': data[1],
                    'modelo': data[2],
                    'tipo': data[3],
                    'color': data[4],
                    'capacidad': data[5],
                    'alto': data[6],
                    'ancho': data[7],
                    'largo': data[8],
                    'id_perfil': data[9],
                    'ano': data[10]
                    
                }
                payload.append(content)
            
            json_data = jsonable_encoder(payload)
            return {"resultado": json_data}
        
        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")  # Devuelve el error al cliente
        
        finally:
            if conn.is_connected():
                conn.close()

    def update_transporte(self, transporte_id: int, transporte: Transporte):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE transporte 
                SET matricula = %s, modelo = %s, tipo = %s, color = %s, capacidad = %s, alto = %s, ancho = %s, largo = %s, ano = %s, id_perfil = %s
                WHERE id = %s
            """, (
                transporte.matricula,
                transporte.modelo,
                transporte.tipo,
                transporte.color,
                transporte.capacidad,
                transporte.alto,
                transporte.ancho,
                transporte.largo,
                transporte.ano,
                transporte.id_perfil,
                transporte_id
            ))

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Transporte no encontrado")

            return {"resultado": "Transporte actualizado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            if conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar el transporte en la base de datos: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def delete_transporte(self, transporte_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM transporte WHERE id = %s", (transporte_id,))

            conn.commit()

            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Transporte no encontrado")

            return {"resultado": "Transporte eliminado exitosamente"}

        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            if conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al eliminar el transporte en la base de datos: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# user_controller = UserController()  # Update this line if necessary
