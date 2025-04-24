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
    phone: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    next_of_kin: Mapped[str] = mapped_column(nullable=True)
    next_of_kin_address: Mapped[str] = mapped_column(nullable=True)
    next_of_kin_phone: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(nullable=True)


class Truck(Base):
    __tablename__ = "truck"

    id: Mapped[int] = mapped_column(primary_key=True)
    plate_number: Mapped[str] = mapped_column(index=True, nullable=True)
    vehicle_model: Mapped[str] = mapped_column(nullable=True)
    tonnage: Mapped[str] = mapped_column(nullable=True)
    driver_name: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    guarantor: Mapped[str] = mapped_column(nullable=True)
    guarantor_phone: Mapped[str] = mapped_column(nullable=True)
    guarantor_address: Mapped[str] = mapped_column(nullable=True)

    trip = relationship('Trip', back_populates='truck')
    expense = relationship('Expense', back_populates='truck')


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True)
    loading_date: Mapped[date] = mapped_column(Date, nullable=True)
    atc_order_number: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    truck_id: Mapped[int] = mapped_column(ForeignKey("truck.id"))
    driver_name: Mapped[str] = mapped_column(nullable=True)
    dispatch: Mapped[int] = mapped_column(nullable=True)
    bonus: Mapped[int] = mapped_column(nullable=True)
    diesel_litres: Mapped[int] = mapped_column(nullable=True)
    diesel_amount: Mapped[int] = mapped_column(nullable=True)
    diesel_date: Mapped[date] = mapped_column(Date, nullable=True)
    customer_name: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[int] = mapped_column(nullable=True)

    truck = relationship('Truck', back_populates='trip')


class Expense(Base):
    __tablename__ = "expense"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    truck_id: Mapped[int] = mapped_column(ForeignKey("truck.id"))
    driver_name: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[int] = mapped_column(nullable=True)

    truck = relationship('Truck', back_populates='expense')
