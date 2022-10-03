import datetime
from enum import Enum
from typing import Optional

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


class TicketUpdate(BaseModel):
    status: TicketStatus


class Ticket(BaseTicket):
    id: int
    user_id: int
    status: TicketStatus
    created_date: datetime.datetime

    class Config:
        orm_mode = True


class BaseMessage(BaseModel):
    message_text: str


class Message(BaseMessage):
    id: int
    user_id: int
    created_date: datetime.datetime

    class Config:
        orm_mode = True
