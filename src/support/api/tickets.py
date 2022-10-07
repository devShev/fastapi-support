from typing import List, Optional

from fastapi import APIRouter, Depends

from support.models.auth import User
from support.models.tickets import (Message, MessageCreate, Ticket,
                                    TicketAttrUpdate, TicketCreate,
                                    TicketStatus, TicketUpdate)
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
    return service.get_tickets_list(user, ticket_status=status)


@router.get('/{ticket_id}', response_model=Ticket)
def get_ticket(
        ticket_id: int,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.get_ticket(user, ticket_id)


@router.post('/', response_model=Ticket)
def create_ticket(
        ticket_data: TicketCreate,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.create_ticket(user, ticket_data)


@router.put('/{ticket_id}', response_model=Ticket)
def update_ticket(
        ticket_id: int,
        ticket_data: TicketUpdate,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.update_ticket(user, ticket_id, ticket_data)


@router.patch('/{ticket_id}', response_model=Ticket)
def update_attr_ticket(
        ticket_id: int,
        ticket_data: TicketAttrUpdate,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.ticket_attr_update(user, ticket_id, ticket_data)


@router.delete('/{ticket_id}')
def delete_ticket(
        ticket_id: int,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.delete_ticket(user, ticket_id)


@router.get('/{ticket_id}/messages', response_model=List[Message])
def get_messages(
        ticket_id: int,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.get_messages(user, ticket_id)


@router.post('/{ticket_id}/messages', response_model=Message)
def create_message(
        ticket_id: int,
        message_text: MessageCreate,
        user: User = Depends(get_current_user),
        service: TicketsService = Depends(),
):
    return service.create_message(user, ticket_id, message_text)
