import datetime
import uuid

from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column, relationship


def _uuid_primary_key() -> str:
    return str(uuid.uuid4())


class DbBaseModel(DeclarativeBase, MappedAsDataclass):
    """DB base model"""
    ...


class UserRole(DbBaseModel):
    __tablename__ = "user_roles"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="RESTRICT"), primary_key=True
    )
    role_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("roles.id", ondelete="RESTRICT"), primary_key=True
    )

    role: Mapped['Role'] = relationship(lazy='selectin', init=False)

    added_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    added_on: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp(), init=False
    )

    @property
    def role_name(self):
        return self.role.name

class User(DbBaseModel):
    """User DB model"""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default_factory=_uuid_primary_key, init=False)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    phone_number: Mapped[int | None] = mapped_column(String(255), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(100))
    role: Mapped['UserRole'] = relationship(foreign_keys=[UserRole.user_id], lazy='selectin', init=False)
    is_email_confirmed: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="FALSE"
    )
    is_phone_confirmed: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="FALSE"
    )
    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True, init=False
    )
    updated_on: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        init=False,
    )

    @property
    def user_info(self) -> dict:
        """Return dict with base user info"""

        full_name = f"{self.first_name} {self.last_name}"
        email = self.email if self.is_email_confirmed else "Not confirmed"
        phone = self.phone_number if self.is_phone_confirmed else "Not confirmed"

        return {
            "full_name": full_name,
            "email": email,
            "phone": phone,
        }


class Role(DbBaseModel):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default_factory=_uuid_primary_key, init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    created_on: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp(), init=False
    )
    created_by: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)

