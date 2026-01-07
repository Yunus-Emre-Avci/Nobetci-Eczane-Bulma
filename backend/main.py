from fastapi import FastAPI, Depends, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List

from fastapi.middleware.cors import CORSMiddleware

import models
import schemas
from database import engine, get_db
import scraper
from config import settings
from scheduler import start_scheduler, stop_scheduler, run_scraping_now

# Template ayarı
templates = Jinja2Templates(directory="templates")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uygulama başlatıldığında scheduler'ı başlat
@app.on_event("startup")
async def startup_event():
    start_scheduler()

# Uygulama kapatıldığında scheduler'ı durdur
@app.on_event("shutdown")
async def shutdown_event():
    stop_scheduler()

# Admin Paneli Arayüzü (GET)
@app.get("/admin")
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

# İşlemi Başlatan Endpoint (Stream)
@app.get("/admin/start-scrape")
async def start_scrape(db: AsyncSession = Depends(get_db)):
    # StreamingResponse, veriyi parça parça (yield edildikçe) tarayıcıya yollar
    return StreamingResponse(
        scraper.scrape_and_save_pharmacies(db), 
        media_type="text/event-stream"
    )

# Manuel Scraping Testi (Scheduler'ı beklemeden hemen çalıştırmak için)
@app.get("/admin/run-scraping-now")
async def manual_scraping():
    """
    Zamanlanmış scraping'i beklemeden hemen çalıştırır (test amaçlı).
    """
    await run_scraping_now()
    return {"message": "Scraping işlemi başlatıldı! Logları kontrol edin."}

# 1. Tüm İlleri Listele
@app.get("/iller/", response_model=List[schemas.IlResponse])
async def get_iller(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Il))
    return result.scalars().all()

# 2. Seçilen İle Göre İlçeleri Listele
@app.get("/iller/{il_id}/ilceler", response_model=List[schemas.IlceResponse])
async def get_ilceler_by_il(il_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Ilce).where(models.Ilce.il_id == il_id))
    ilceler = result.scalars().all()
    if not ilceler:
        return [] # Boş liste dön
    return ilceler

# 3. Tüm Eczaneleri Listele (İl ve İlçe bilgisiyle beraber)
@app.get("/eczaneler/", response_model=List[schemas.EczaneResponse])
async def get_eczaneler(db: AsyncSession = Depends(get_db)):
    # Eager Loading: Eczaneyi çekerken bağlı olduğu il ve ilçeyi de tek sorguda getir (N+1 problemini önler)
    query = select(models.Eczane).options(
        selectinload(models.Eczane.il),
        selectinload(models.Eczane.ilce)
    )
    result = await db.execute(query)
    return result.scalars().all()