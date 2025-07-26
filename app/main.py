from fastapi import FastAPI
from app.routes.usuario_routes import router as usuario_router
from app.routes.transporte_routes import router as transporte_router  
from app.routes.perfil_routes import router as perfil_router  
from app.routes.atributo_routes import router as atributo_router  
from app.routes.atributo_usuario_routes import router as atributo_usuario_router  
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    #"http://localhost.tiangolo.com",
    #"https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:4200"
    #"http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario_router)
app.include_router(transporte_router)  
app.include_router(perfil_router) 
app.include_router(atributo_router)  
app.include_router(atributo_usuario_router)  

#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000)

