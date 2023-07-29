from fastapi import APIRouter, UploadFile, File, Form
from starlette import status
from models import network_analyze
networks_router = APIRouter()
networks = [
    {
        "name": "Network 1",
        "id": 1,
        "type": "ethernet",
        "subnet": "10.0.0.0/24",
        "gateway": "10.0.0.1",
    },
    {
        "name": "Network 2",
        "id": 2,
        "type": "wifi",
        "subnet": "192.168.1.0/24",
        "gateway": "192.168.1.1",
    },
]


@networks_router.get("/", status_code=status.HTTP_200_OK)
async def get_networks():
    return networks


@networks_router.get("/id/{network_id}", status_code=status.HTTP_200_OK)
async def get_network_by_id(network_id):
    return [network for network in networks if network['id'] == int(network_id)][0]


@networks_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_network(capture_file: UploadFile = File(...),
                         client_id: str = Form(...),
                         data_taken: str = Form(...),
                         location_name: str = Form(...),):
    a = network_analyze.capture_analyze(capture_file)
    return {"packets": a, "client_id": client_id}


