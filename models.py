from sqlalchemy import (
    BigInteger,
    Column, DateTime,
    ForeignKey,
    func,
    SmallInteger,
    String
)
from sqlalchemy.orm import relationship, validates

from database import Base


class Bot(Base):
    __tablename__ = 'bot'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=True)
    discriminator = Column(String(4), nullable=True)
    display_name = Column(String(64), nullable=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=False)
    msg_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    user = relationship('User')
    cohort = relationship('Cohort')

    @validates('id')
    def validate_id(self, key, id):
        if type(id) is not int:
            raise TypeError

        if len(str(id)) != 18:
            raise ValueError

        return id

    @validates('name')
    def validate_name(self, key, name):
        if type(name) is not str:
            raise TypeError

        if len(name) > 64:
            raise ValueError

        return name

    @validates('discriminator')
    def validate_discriminator(self, key, discriminator):
        if type(discriminator) is not str:
            raise TypeError

        if len(discriminator) != 4:
            raise ValueError

        return discriminator

    @validates('display_name')
    def validate_display_name(self, key, display_name):
        if type(display_name) is not str:
            raise TypeError

        if len(display_name) > 64:
            raise ValueError

        return display_name

    @validates('user_id')
    def validate_user_id(self, key, user_id):
        if type(user_id) is not int:
            raise TypeError

        if len(str(user_id)) != 18:
            raise ValueError

        return user_id

    @validates('cohort_id')
    def validate_cohort_id(self, key, cohort_id):
        if type(cohort_id) is not int:
            raise TypeError

        return cohort_id

    @validates('msg_id')
    def validate_msg_id(self, key, msg_id):
        if type(msg_id) is not int:
            raise TypeError

        if len(str(msg_id)) != 18:
            raise ValueError

        return msg_id


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)


class Cohort(Base):
    __tablename__ = 'cohort'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    nickname = Column(String(16), nullable=False)
