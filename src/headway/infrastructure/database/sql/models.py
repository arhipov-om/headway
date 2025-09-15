from __future__ import annotations

from datetime import datetime, time
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    String,
    Boolean,
    DateTime,
    Time, MetaData,
)
from sqlalchemy.dialects.postgresql import UUID as SQL_UUID
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    timezone: Mapped[str] = mapped_column(String)

    identities: Mapped[list[IdentityORM]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    reminders: Mapped[list[ReminderORM]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return "<UserORM(id={}, name={}, timezone={}, identities={})>".format(
            self.id, self.name, self.timezone, self.identities)


class IdentityORM(Base):
    __tablename__ = "identities"

    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    provider_id: Mapped[str] = mapped_column(String, nullable=False)
    provider: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped[UserORM] = relationship(back_populates="identities")


class MotivationORM(Base):
    __tablename__ = "motivations"

    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)


class ReminderORM(Base):
    __tablename__ = "reminders"

    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(String, nullable=False)
    frequency: Mapped[str] = mapped_column(String, nullable=False)
    start_day: Mapped[int | None]
    days: Mapped[str | None]
    time: Mapped[time] = mapped_column(Time, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean)

    user: Mapped[UserORM] = relationship(back_populates="reminders")
    notifications: Mapped[list[NotificationORM]] = relationship(
        back_populates="reminder",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return "ReminderORM<(id={} user_id={}, text={}, frequency={}, start_day={}, days={}, time={})>".format(
            self.id, self.user_id, self.text, self.frequency, self.start_day, self.days, self.time
        )

class NotificationORM(Base):
    __tablename__ = "notifications"

    id: Mapped[UUID] = mapped_column(SQL_UUID(as_uuid=True), primary_key=True)
    reminder_id: Mapped[UUID] = mapped_column(ForeignKey("reminders.id", ondelete="CASCADE"))
    scheduled_for: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sent: Mapped[bool] = mapped_column(Boolean)
    motivation_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("motivations.id", ondelete="SET NULL"), nullable=True
    )

    reminder: Mapped[ReminderORM] = relationship(back_populates="notifications")
    motivation: Mapped[MotivationORM | None] = relationship()
