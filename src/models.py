from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, Integer


class Base(DeclarativeBase):
    pass


class WasteType(Base):
    __tablename__ = "waste_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column(String(255))

    fullness: Mapped[list["Fullness"]] = relationship("Fullness", back_populates="waste_type")


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[float] = mapped_column(Float())
    longitude: Mapped[float] = mapped_column(Float())

    fullness: Mapped[list["Fullness"]] = relationship(
        "Fullness",
        back_populates="organization",
        cascade="all, delete-orphan"
    )


class Storage(Base):
    __tablename__ = "storages"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[float] = mapped_column(Float())
    longitude: Mapped[float] = mapped_column(Float())

    fullness: Mapped[list["Fullness"]] = relationship(
        "Fullness",
        back_populates="storage",
        cascade="all, delete-orphan"
    )


class Fullness(Base):
    __tablename__ = "fullness"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[Optional[int]] = mapped_column(ForeignKey('organizations.id'), nullable=True)
    storage_id: Mapped[Optional[int]] = mapped_column(ForeignKey('storages.id'), nullable=True)
    waste_type_id: Mapped[int] = mapped_column(ForeignKey('waste_types.id'))
    current_fill: Mapped[int] = mapped_column(Integer)
    capacity: Mapped[int] = mapped_column(Integer)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="fullness")
    storage: Mapped["Storage"] = relationship("Storage", back_populates="fullness")
    waste_type: Mapped["WasteType"] = relationship("WasteType", back_populates="fullness")
