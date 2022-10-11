from typing import List, Optional

from celery_app.support.tasks import send_status_to_mail
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from support import tables
from support.database import get_session
from support.models.auth import User, UserGroup
from support.models.tickets import (Message, MessageCreate, Ticket,
                                    TicketAttrUpdate, TicketCreate,
                                    TicketStatus, TicketUpdate)


class Tools:
    @staticmethod
    def check_moder_or_owner(user: User, ticket: tables.Ticket) -> None:
        """
        Give access to ticket if user is owner or moder
        """

        if not (user.id == ticket.user_id or user.user_group == UserGroup.MODER):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def check_moder_fields(user: User, field: str) -> None:
        """
        Checking access to changing field
        """

        only_moder_fields = (
            'id',
            'status',
            'user_id',
            'created_date',
        )

        if user.user_group != UserGroup.MODER and (field in only_moder_fields):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def check_the_status_change(init_status: str, ticket: Ticket, session: Session):
        """
        Checking init & current status. If current != init - send message to ticket owner
        """

        if ticket.status != init_status:
            ticket_owner = session.query(tables.User).filter_by(id=ticket.user_id).first()
            email = ticket_owner.email
            if email:
                send_status_to_mail.delay(email, ticket.status)


class TicketsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_ticket(self, user: User, ticket_id: int) -> tables.Ticket:
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

        Tools.check_moder_or_owner(user, ticket)

        return ticket

    def get_ticket(self, user: User, ticket_id: int) -> tables.Ticket:
        return self._get_ticket(user, ticket_id)

    def get_tickets_list(self, user: User, ticket_status: Optional[TicketStatus] = None) -> List[tables.Ticket]:
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

    def create_ticket(self, user: User, ticket_data: TicketCreate) -> tables.Ticket:
        ticket = tables.Ticket(
            **ticket_data.dict(),
            user_id=user.id,
            status=TicketStatus.active,
        )

        self.session.add(ticket)
        self.session.commit()

        return ticket

    def update_ticket(self, user: User, ticket_id: int, ticket_data: TicketUpdate) -> tables.Ticket:
        ticket = self._get_ticket(user, ticket_id)

        init_status = ticket.status

        for field, value in ticket_data:
            setattr(ticket, field, value)

        if user.user_group == UserGroup.USER:
            ticket.status = init_status

        Tools.check_the_status_change(init_status, ticket, self.session)

        self.session.commit()

        return ticket

    def ticket_attr_update(self, user: User, ticket_id: int, ticket_data: TicketAttrUpdate) -> tables.Ticket:
        ticket = self._get_ticket(user, ticket_id)

        init_status = ticket.status

        field = ticket_data.field
        value = ticket_data.value

        if not hasattr(ticket, field):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        Tools.check_moder_fields(user, field)

        setattr(ticket, field, value)

        Tools.check_the_status_change(init_status, ticket, self.session)

        self.session.commit()

        return ticket

    def delete_ticket(self, user: User, ticket_id: int) -> None:
        ticket = self._get_ticket(user, ticket_id)

        self.session.delete(ticket)
        self.session.commit()

    def create_message(self, user, ticket_id: int, message_data: MessageCreate) -> Message:
        ticket = self._get_ticket(user, ticket_id)

        Tools.check_moder_or_owner(user, ticket)

        message = tables.Message(
            **message_data.dict(),
            ticket_id=ticket_id,
            user_id=user.id,
        )

        self.session.add(message)
        self.session.commit()

        return message

    def get_messages(self, user: User, ticket_id: int) -> List[tables.Message]:
        ticket = self._get_ticket(user, ticket_id)

        Tools.check_moder_or_owner(user, ticket)  # Check permissions (invalid = raise 404)

        query = (
            self.session
            .query(tables.Message)
            .filter_by(ticket_id=ticket_id)
        )

        tickets = query.all()

        return tickets
