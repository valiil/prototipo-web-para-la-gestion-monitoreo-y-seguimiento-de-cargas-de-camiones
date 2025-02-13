import mysql.connector
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.modulo_model import Modulo
from fastapi.encoders import jsonable_encoder

class ModuloController:
    
    def get_modulos_por_perfil(self, perfil_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT m.id, m.nombre, m.descripcion, mp.activo
                FROM modulo m
                JOIN modulo_por_perfil mp ON m.id = mp.modulo_id
                WHERE mp.perfil_id = %s
            """, (perfil_id,))
            result = cursor.fetchall()
            
            if not result:
                raise HTTPException(status_code=404, detail="No hay módulos asignados para este perfil")
            
            modulos = []
            for data in result:
                modulo = {
                    'id': data[0],
                    'nombre': data[1],
                    'descripcion': data[2],
                    'activo': bool(data[3])  # Convertimos el valor de 'activo' en un booleano
                }
                modulos.append(modulo)
            
            return jsonable_encoder({"resultado": modulos})
        
        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            if conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al obtener los módulos: {err}")
        
        finally:
            if conn.is_connected():
                conn.close()

    def actualizar_estado_modulo(self, modulo_id: int, perfil_id: int, estado: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar si el módulo y perfil existen
            cursor.execute("""
                SELECT 1
                FROM modulo_por_perfil
                WHERE modulo_id = %s AND perfil_id = %s
            """, (modulo_id, perfil_id))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail="El módulo no está asignado a este perfil")
            
            # Actualizar el estado del módulo
            cursor.execute("""
                UPDATE modulo_por_perfil
                SET activo = %s
                WHERE modulo_id = %s AND perfil_id = %s
            """, (estado, modulo_id, perfil_id))
            conn.commit()
            
            # Verificar si se actualizó algún registro
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="No se pudo actualizar el estado del módulo")
            
            return {"mensaje": "Módulo actualizado correctamente"}
        
        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            if conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error al actualizar el módulo: {err}")
        
        finally:
            if conn.is_connected():
                conn.close()
