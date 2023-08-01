from fastapi import APIRouter, UploadFile, File, Form, Depends
from starlette import status
from models import network_analyze
from models.authentication2 import get_current_technician

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
async def get_networks(active_technician=Depends(get_current_technician)):
    return networks


@networks_router.get("/id/{network_id}", status_code=status.HTTP_200_OK)
async def get_network_by_id(network_id, active_technician=Depends(get_current_technician)):
    # [network for network in networks if network['id'] == int(network_id)][0]
    pass


@networks_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_network(capture_file: UploadFile = File(...),
                         client_id: str = Form(...),
                         date_taken: str = Form(...),
                         location_name: str = Form(...),
                         active_technician=Depends(get_current_technician), ):
    packets = network_analyze.create_network(capture_file, client_id, date_taken, location_name)
    return {"packets": packets, "client_id": client_id}
