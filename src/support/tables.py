import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.Text, unique=True)
    username = sa.Column(sa.Text, unique=True)
    password_hash = sa.Column(sa.Text)
    user_group = sa.Column(sa.String, default='user')


class Ticket(Base):
    __tablename__ = 'tickets'

    id = sa.Column(sa.Integer, primary_key=True)
    subject = sa.Column(sa.Text, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    description = sa.Column(sa.Text)
    status = sa.Column(sa.Text)
    created_date = sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.utcnow)


class Message(Base):
    __tablename__ = 'messages'

    id = sa.Column(sa.Integer, primary_key=True)
    ticket_id = sa.Column(sa.Integer, sa.ForeignKey('tickets.id'))
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    message_text = sa.Column(sa.Text)
    created_date = sa.Column(sa.DateTime(timezone=True), default=datetime.datetime.utcnow)
