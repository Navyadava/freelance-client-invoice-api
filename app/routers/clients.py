from fastapi import APIRouter, HTTPException

from app.schemas import ClientCreate, ClientResponse


router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

clients = []


@router.post("/", response_model=ClientResponse, status_code=201)
def create_client(client: ClientCreate):
    new_client = {
        "id": len(clients) + 1,
        **client.model_dump()
    }

    clients.append(new_client)

    return new_client


@router.get("/", response_model=list[ClientResponse])
def get_clients():
    return clients


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int):
    for client in clients:
        if client["id"] == client_id:
            return client

    raise HTTPException(
        status_code=404,
        detail="Client not found"
    )