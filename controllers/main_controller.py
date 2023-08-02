from fastapi import FastAPI
from fastapi import Request, Response
import uvicorn
from models.DB_connection import create_server_connection
from technician_controller import technicians_router
from network_controller import networks_router

app = FastAPI()

app.include_router(networks_router, prefix="/networks", tags=["networks"], )
app.include_router(technicians_router, prefix="/technicians", tags=["technicians"], )


@app.on_event("startup")
def startup():
    create_server_connection()


@app.on_event("shutdown")
def shutdown():
    disconnect()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
