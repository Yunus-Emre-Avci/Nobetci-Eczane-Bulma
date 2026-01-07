"""
Otomatik Scraping Zamanlayıcı
Her gün saat 09:00'da (TR İstanbul saati) scraping işlemini otomatik olarak çalıştırır.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from datetime import datetime
import asyncio
from database import async_session
from scraper import scrape_and_save_pharmacies
import logging

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Türkiye saat dilimi
TR_TZ = timezone('Europe/Istanbul')

# Scheduler instance
scheduler = AsyncIOScheduler(timezone=TR_TZ)

async def scheduled_scraping_task():
    """
    Zamanlanmış scraping görevi.
    Her gün 09:00'da otomatik olarak çalışır.
    """
    logger.info(f"🕒 Otomatik scraping başlatıldı - {datetime.now(TR_TZ).strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Async session oluştur
        async with async_session() as db:
            # Scraping işlemini çalıştır (generator olduğu için consume etmemiz gerekiyor)
            async for log_message in scrape_and_save_pharmacies(db):
                # Log mesajlarını yazdır
                if log_message.startswith("PROGRESS"):
                    parts = log_message.split("|")
                    if len(parts) >= 3:
                        logger.info(f"📊 İlerleme: %{parts[1]} - {parts[2].strip()}")
                else:
                    logger.info(f"📝 {log_message.strip()}")
        
        logger.info("✅ Otomatik scraping başarıyla tamamlandı!")
        
    except Exception as e:
        logger.error(f"❌ Otomatik scraping hatası: {e}")

def start_scheduler():
    """
    Scheduler'ı başlatır ve zamanlanmış görevi ekler.
    Her gün saat 09:00'da çalışacak şekilde ayarlanır.
    """
    # Cron trigger: Her gün saat 09:00'da çalış
    trigger = CronTrigger(
        hour=9,
        minute=0,
        timezone=TR_TZ
    )
    
    # Görevi scheduler'a ekle
    scheduler.add_job(
        scheduled_scraping_task,
        trigger=trigger,
        id='daily_pharmacy_scraping',
        name='Günlük Eczane Scraping',
        replace_existing=True
    )
    
    # Scheduler'ı başlat
    scheduler.start()
    
    logger.info("🚀 Scheduler başlatıldı!")
    logger.info(f"⏰ Scraping her gün saat 09:00'da (TR İstanbul saati) otomatik olarak çalışacak")
    
    # Bir sonraki çalışma zamanını göster
    next_run = scheduler.get_job('daily_pharmacy_scraping').next_run_time
    logger.info(f"📅 Bir sonraki çalışma zamanı: {next_run.strftime('%Y-%m-%d %H:%M:%S %Z')}")

def stop_scheduler():
    """
    Scheduler'ı durdurur.
    """
    scheduler.shutdown()
    logger.info("🛑 Scheduler durduruldu!")

# Manuel test için endpoint
async def run_scraping_now():
    """
    Scraping'i hemen çalıştırmak için kullanılabilir (test amaçlı).
    """
    logger.info("🔧 Manuel scraping başlatıldı...")
    await scheduled_scraping_task()
