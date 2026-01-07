from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- İL ŞEMALARI ---
class IlBase(BaseModel):
    baslik: str
    slug: str

class IlResponse(IlBase):
    id: int
    class Config:
        from_attributes = True

# --- İLÇE ŞEMALARI ---
class IlceBase(BaseModel):
    baslik: str
    slug: str
    il_id: int

class IlceResponse(IlceBase):
    id: int
    class Config:
        from_attributes = True

# --- ECZANE ŞEMALARI ---
# Ortak özellikler (Sadece okuma amaçlı kullanılacak)
class EczaneBase(BaseModel):
    eczane_adi: str
    adres: str
    telefon: Optional[str] = None
    il_id: int
    ilce_id: int

# Kullanıcıya dönecek tam veri seti
class EczaneResponse(EczaneBase):
    id: int
    olusturulma_tarihi: datetime
    
    # Eczaneyi çekerken hangi il ve ilçede olduğunu da gösterelim
    il: Optional[IlResponse] = None
    ilce: Optional[IlceResponse] = None

    class Config:
        from_attributes = True