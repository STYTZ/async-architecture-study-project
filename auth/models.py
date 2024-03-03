import enum

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class DbBase(DeclarativeBase):
    pass


class Role(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    ACCOUNTANT = "accountant"


class User(DbBase):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str]
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str]
    role: Mapped[Role]
