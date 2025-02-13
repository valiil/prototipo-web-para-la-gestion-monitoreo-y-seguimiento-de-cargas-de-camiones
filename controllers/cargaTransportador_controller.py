from fastapi import HTTPException
from typing import Optional
from datetime import datetime
import mysql.connector
from config.db_config import get_db_connection
from fastapi.encoders import jsonable_encoder
from models.cargaTransportador_model import CargaPorTransportador

class CargaTransportadorController:
    
    def get_cargas_por_transportador(self, transportador_id: int, start_date: Optional[str] = None, end_date: Optional[str] = None):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Si start_date y end_date son proporcionados, usarlos para filtrar las fechas
            query = """
                SELECT c.id, c.peso, c.largo, c.ancho, c.alto, c.tipo,
                       c.fecha_recogida, c.fecha_entrega, c.estado_actual,
                       c.origen, c.destino, c.descripcion
                FROM envio e
                JOIN carga c ON e.id_carga = c.id
                WHERE e.id_transportador = %s
            """
            
            # Si se proporcionan las fechas, añadirlas al filtro
            if start_date and end_date:
                query += " AND c.fecha_recogida BETWEEN %s AND %s"
            
            cursor.execute(query, (transportador_id, start_date, end_date) if start_date and end_date else (transportador_id,))
            result = cursor.fetchall()
            
            if not result:
                raise HTTPException(status_code=404, detail="No se encontraron cargas para el transportador especificado")
            
            cargas = []
            for data in result:
                carga = CargaPorTransportador(
                    id=data[0],
                    peso=data[1],
                    largo=data[2],
                    ancho=data[3],
                    alto=data[4],
                    tipo=data[5],
                    fecha_recogida=data[6],
                    fecha_entrega=data[7],
                    estado_actual=data[8],
                    origen=data[9],
                    destino=data[10],
                    descripcion=data[11]
                )
                cargas.append(carga)
            
            json_data = jsonable_encoder(cargas)
            return {"resultado": json_data}
        
        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            if conn.is_connected():
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Error de base de datos: {err}")
        
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
