from fastapi import FastAPI
import uvicorn
from technician_controller import technicians_router
from network_controller import networks_router

app = FastAPI()

app.include_router(networks_router, prefix="/networks", tags=["networks"], )
app.include_router(technicians_router, prefix="/technicians", tags=["technicians"], )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
