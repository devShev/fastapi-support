import datetime
from enum import Enum

from pydantic import BaseModel


class TicketStatus(str, Enum):
    active = 'active'
    solved = 'solved'
    unsolved = 'unsolved'
    frozen = 'frozen'


class BaseTicket(BaseModel):
    subject: str
    description: str


class TicketCreate(BaseTicket):
    pass


class TicketUpdate(BaseTicket):
    status: str


class TicketAttrUpdate(BaseModel):
    field: str
    value: str


class Ticket(BaseTicket):
    id: int
    user_id: int
    status: TicketStatus
    created_date: datetime.datetime

    class Config:
        orm_mode = True


class BaseMessage(BaseModel):
    message_text: str


class MessageCreate(BaseMessage):
    pass


class Message(BaseMessage):
    id: int
    ticket_id: int
    user_id: int
    created_date: datetime.datetime

    class Config:
        orm_mode = True
