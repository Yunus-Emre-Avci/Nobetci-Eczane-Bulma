from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Il(Base):
    __tablename__ = "iller"

    id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)

    # İlişkiler: Bir ilin birden fazla ilçesi ve eczanesi olabilir
    ilceler = relationship("Ilce", back_populates="il")
    eczaneler = relationship("Eczane", back_populates="il")

class Ilce(Base):
    __tablename__ = "ilceler"

    id = Column(Integer, primary_key=True, index=True)
    il_id = Column(Integer, ForeignKey("iller.id", ondelete="CASCADE"), nullable=False)
    baslik = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)

    # İlişkiler
    il = relationship("Il", back_populates="ilceler")
    eczaneler = relationship("Eczane", back_populates="ilce")

class Eczane(Base):
    __tablename__ = "eczaneler"

    id = Column(Integer, primary_key=True, index=True)
    il_id = Column(Integer, ForeignKey("iller.id"), nullable=False)
    ilce_id = Column(Integer, ForeignKey("ilceler.id"), nullable=False)
    eczane_adi = Column(String(150), nullable=False)
    adres = Column(Text, nullable=False)
    telefon = Column(String(20), nullable=True)
    olusturulma_tarihi = Column(DateTime(timezone=True), server_default=func.now())

    # İlişkiler: Eczane hem bir ile hem bir ilçeye bağlıdır
    il = relationship("Il", back_populates="eczaneler")
    ilce = relationship("Ilce", back_populates="eczaneler")