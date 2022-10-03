from typing import Optional, List

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from support import tables
from support.database import get_session
from support.models.auth import User, UserGroup
from support.models.tickets import TicketStatus, TicketCreate, TicketUpdate


class TicketsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, user: User, ticket_id: int) -> tables.Ticket:
        ticket = (
            self.session
            .query(tables.Ticket)
            .filter_by(
                id=ticket_id,
            )
            .first()
        )

        if not ticket:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        if user.user_group != UserGroup.MODER and ticket.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return ticket

    def get(self, user: User, ticket_id: int) -> tables.Ticket:
        return self._get(user, ticket_id)

    def get_list(self, user: User, ticket_status: Optional[TicketStatus] = None) -> List[tables.Ticket]:
        query = (
            self.session
            .query(tables.Ticket)
        )

        if user.user_group == UserGroup.USER:
            query = query.filter_by(user_id=user.id)

        if ticket_status:
            query = query.filter_by(status=ticket_status)

        tickets = query.all()

        return tickets

    def create(self, user: User, ticket_data: TicketCreate) -> tables.Ticket:
        ticket = tables.Ticket(
            **ticket_data.dict(),
            user_id=user.id,
            status=TicketStatus.active,
        )

        self.session.add(ticket)
        self.session.commit()

        return ticket

    def update(self, user: User, ticket_id: int, ticket_data: TicketUpdate) -> tables.Ticket:
        ticket = self._get(user, ticket_id)

        init_status = ticket.status

        ticket.status = ticket_data.status

        if user.user_group == UserGroup.USER:
            ticket.status = init_status

        self.session.commit()

        return ticket

    def delete(self, user: User, ticket_id: int):
        ticket = self._get(user, ticket_id)

        self.session.delete(ticket)
        self.session.commit()
