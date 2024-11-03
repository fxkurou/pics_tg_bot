from pydantic_core.core_schema import nullable_schema
from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True)
    is_registered: Mapped[bool] = mapped_column(default=False)

    pictures: Mapped[list["Picture"]] = relationship("Picture", back_populates="user")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="users")

    def __repr__(self):
        return f'<User {self.username}, username {self.username}, is_registered {self.is_registered}>'


class Picture(Base):
    __tablename__ = 'pictures'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_tg_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'), nullable=False)
    file_id: Mapped[str] = mapped_column(nullable=False)
    tag_name: Mapped[str] = mapped_column(ForeignKey('tags.name'), nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)
    payment_id: Mapped[int] = mapped_column(ForeignKey('payments.id'), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="pictures")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="pictures")
    payment: Mapped["Payment"] = relationship("Payment", back_populates="pictures")

    def __repr__(self):
        return f'<Picture {self.id}, user_id {self.user_tg_id}, file_id {self.file_id},tags {self.tag}>'


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    pictures: Mapped[list["Picture"]] = relationship("Picture", back_populates="tag")

    def __repr__(self):
        return f'<Tag {self.name}>'


class Donation(Base):
    __tablename__ = 'donations'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    order_id: Mapped[str] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(nullable=False)
    total_amount: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self):
        return f'<Donation {self.id}, user_id {self.user_id}, order_id {self.order_id}, total_amount {self.total_amount}>'


class Payment(Base):
    __tablename__ = 'payments'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'), nullable=False)
    order_id: Mapped[str] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(nullable=False)
    total_amount: Mapped[int] = mapped_column(nullable=False)

    pictures: Mapped[list["Picture"]] = relationship("Picture", back_populates="payment")
    users: Mapped["User"] = relationship("User", back_populates="payments")

    def __repr__(self):
        return f'<Payment {self.id}, user_id {self.user_id}, order_id {self.order_id}, total_amount {self.total_amount}>'