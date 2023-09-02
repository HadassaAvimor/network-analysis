from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Response
from starlette import status
from models import network_analyze
from models.authn_authz import get_current_technician, authorize_technician

networks_router = APIRouter()


@networks_router.get("/id/{network_id}", status_code=status.HTTP_200_OK)
async def get_network_by_id(network_id):
    return network_analyze.get_network_by_id(network_id)


@networks_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_network(capture_file: UploadFile = File(...),
                         client_id: str = Form(...),
                         location_name: str = Form(...), ):
    # active_technician = authorize_technician(client_id)
    # if active_technician is None:
    #     return HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    network_id, network_visualisation = await network_analyze.create_network(capture_file, client_id, location_name)
    return Response(content=network_visualisation.getvalue(), media_type="image/png")
