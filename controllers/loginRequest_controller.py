import mysql.connector
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.loginRequest_model import LoginRequest  

class LoginRequestController:

    def login(self, login_request: LoginRequest):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar las credenciales del usuario
            cursor.execute("""SELECT id_perfil, nombre FROM usuario WHERE usuario = %s AND contrasena = %s""",
                           (login_request.usuario, login_request.contrasena))
            
            result = cursor.fetchone()

            if result:
                id_perfil, nombre = result
                
                # Determinar el tipo de usuario
                if id_perfil == 1:
                    tipo_usuario = "Administrador"
                elif id_perfil == 2:
                    tipo_usuario = "Transportador"
                elif id_perfil == 3:
                    tipo_usuario = "Empresa"
                elif id_perfil == 4:
                    tipo_usuario = "Operador Logistico"
                else:
                    raise HTTPException(status_code=400, detail="Tipo de usuario no válido")
                
                return {
                    "mensaje": f"Credenciales válidas para {tipo_usuario}",
                    "tipo_usuario": tipo_usuario,
                    "nombre": nombre,
                    "id_perfil": id_perfil  # Asegúrate de incluir el id_perfil en la respuesta
                }
            else:
                raise HTTPException(status_code=401, detail="Credenciales inválidas")

        except mysql.connector.Error as err:
            print(f"Error en la base de datos: {err}")
            raise HTTPException(status_code=500, detail=f"Error en la base de datos: {err}")

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
