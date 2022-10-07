from typing import List, Optional

from fastapi import APIRouter, Depends

from support.models.tickets import Ticket, TicketStatus, TicketCreate, TicketUpdate, TicketAttrUpdate
from support.models.auth import User
from support.services.auth import get_current_user
from support.services.tickets import TicketsService

router = APIRouter(
    prefix='/tickets',
    tags=['Tickets'],
)


@router.get('/', response_model=List[Ticket])
def get_tickets(
        status: Optional[TicketStatus] = None,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.get_list(user, ticket_status=status)


@router.get('/{ticket_id}', response_model=Ticket)
def get_ticket(
        ticket_id: int,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.get(user, ticket_id)


@router.post('/', response_model=Ticket)
def create_ticket(
        ticket_data: TicketCreate,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.create(user, ticket_data)


@router.put('/{ticket_id}', response_model=Ticket)
def update_ticket(
        ticket_id: int,
        ticket_data: TicketUpdate,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.update(user, ticket_id, ticket_data)


@router.patch('/{ticket_id}', response_model=Ticket)
def update_attr_ticket(
        ticket_id: int,
        ticket_data: TicketAttrUpdate,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.attr_update(user, ticket_id, ticket_data)


@router.delete('/{ticket_id}')
def delete(
        ticket_id: int,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.delete(user, ticket_id)
