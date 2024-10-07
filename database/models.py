from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True)
    is_registered: Mapped[bool] = mapped_column(default=False)

    pictures: Mapped[list["Picture"]] = relationship("Picture", back_populates="user")

    def __repr__(self):
        return f'<User {self.username}, username {self.username}, is_registered {self.is_registered}>'


class Picture(Base):
    __tablename__ = 'pictures'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_tg_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'), nullable=False)
    file_id: Mapped[str] = mapped_column(nullable=False)
    tag: Mapped[str] = mapped_column()
    file_path: Mapped[str] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="pictures")

    def __repr__(self):
        return f'<Picture {self.id}, user_id {self.user_tg_id}, file_id {self.file_id},tags {self.tag}>'


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    pictures: Mapped[list["Picture"]] = relationship("Picture", back_populates="tag")

    def __repr__(self):
        return f'<Tag {self.name}>'