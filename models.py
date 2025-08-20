from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, String, ForeignKey, DateTime, func

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str|None] = mapped_column(String(64))
    ref_code: Mapped[str] = mapped_column(String(12), unique=True)
    referred_by: Mapped[int|None] = mapped_column(ForeignKey('users.id'))
    balance_cents: Mapped[int] = mapped_column(Integer, default=0)
    vip_level: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped = mapped_column(DateTime, server_default=func.now())