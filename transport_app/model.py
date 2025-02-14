from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date
from transport_app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=True)
    full_name: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=True)
    user_type: Mapped[str] = mapped_column(nullable=True)


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    plate_number: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)

    trip = relationship('Trip', back_populates='driver')
    expense = relationship('Expense', back_populates='driver')


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)
    loading_date: Mapped[date] = mapped_column(Date, nullable=True)
    atc_order_number: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    driver_name: Mapped[str] = mapped_column(nullable=True)
    dispatch: Mapped[int] = mapped_column(nullable=True)
    bonus: Mapped[int] = mapped_column(nullable=True)
    diesel_litres: Mapped[int] = mapped_column(nullable=True)
    diesel_amount: Mapped[int] = mapped_column(nullable=True)
    diesel_date: Mapped[date] = mapped_column(Date, nullable=True)
    customer_name: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[int] = mapped_column(nullable=True)

    driver = relationship('Driver', back_populates='trip')


class Expense(Base):
    __tablename__ = "expense"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id"))
    driver_name: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[int] = mapped_column(nullable=True)

    driver = relationship('Driver', back_populates='expense')
