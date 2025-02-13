from fastapi import FastAPI
from routes.usuario_routes import router as usuario_router
from routes.transporte_routes import router as transporte_router  
from routes.perfil_routes import router as perfil_router  
from routes.atributo_routes import router as atributo_router  
from routes.atributo_usuario_routes import router as atributo_usuario_router  
from routes.carga_masiva_routes import router as carga_masiva_router
from routes.carga_routes import router as carga_router
from routes.loginRequest_routes import router as loginRequest_router
from routes.cargaTransportador_routes import router as cargaTransportador_router
from routes.cargaEmpresa_routes import router as cargaEmpresa_router
from routes.envio_routes import router as envio_router
from routes.token_routes import router as token_router
from routes.modulo_routes import router as modulo_routes
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

origins = [
    #"http://localhost.tiangolo.com",
    #"https://localhost.tiangolo.com",
    "http://localhost"
    #"http://localhost:8080",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router)
app.include_router(transporte_router)  
app.include_router(perfil_router) 
app.include_router(atributo_router)  
app.include_router(atributo_usuario_router) 
app.include_router(carga_masiva_router)
app.include_router(carga_router) 
app.include_router(loginRequest_router)  
app.include_router(cargaTransportador_router) 
app.include_router(cargaEmpresa_router) 
app.include_router(envio_router)
app.include_router(token_router)
app.include_router(modulo_routes)



if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, host="0.0.0.0", port=8000)

