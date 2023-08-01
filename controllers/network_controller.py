from fastapi import APIRouter, UploadFile, File, Form
from starlette import status
from models import network_analyze

networks_router = APIRouter()


@networks_router.get("/", status_code=status.HTTP_200_OK)
async def get_networks():
    # TODO invoke function of get networks from db
    pass


@networks_router.get("/id/{network_id}", status_code=status.HTTP_200_OK)
async def get_network_by_id(network_id):
    # TODO invoke function of get network by id from db
    pass


@networks_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_network(capture_file: UploadFile = File(...),
                         client_id: str = Form(...),
                         location_name: str = Form(...), ):
    network = network_analyze.create_network(capture_file, client_id, location_name)
    return {"network": network}
