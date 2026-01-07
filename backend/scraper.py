import requests
from bs4 import BeautifulSoup
from sqlalchemy.future import select
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import models

async def scrape_and_save_pharmacies(db: AsyncSession):
    # 1. ADIM: Mevcut Eczaneleri Temizle (TRUNCATE)
    # Eczaneler tablosunu sıfırlar (ID'leri de sıfırlamak için RESTART IDENTITY)
    try:
        await db.execute(text("TRUNCATE TABLE eczaneler RESTART IDENTITY CASCADE"))
        await db.commit()
        yield "Veritabanı temizlendi... %0\n"
    except Exception as e:
        yield f"Tablo temizleme hatası: {e}\n"
        return

    # 2. ADIM: İl ve İlçeleri Çek
    # Veritabanından tüm il ve ilçeleri hiyerarşik olarak çekiyoruz
    stmt = select(models.Ilce).join(models.Il)
    result = await db.execute(stmt)
    ilceler = result.scalars().all()
    
    total_count = len(ilceler)
    yield f"Toplam {total_count} ilçe taranacak... Hazırlanıyor.\n"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # 3. ADIM: Döngü ve Scraping
    processed_count = 0
    
    for ilce in ilceler:
        # DB ilişkisinden il slug'ını almamız lazım (Lazy loading yerine select'te join attık ama buradan erişmek için await gerekebilir, 
        # bu yüzden basitlik adına ilçe nesnesinden il_id ile tekrar çekmek yerine yukarıdaki join mantığını kullanacağız)
        
        # URL Oluşturma Mantığı: https://www.eczaneler.gen.tr/nobetci-{il}-{ilce}
        # Örn: nobetci-istanbul-sisli
        # Not: models.py'da relationship tanımlı olduğu için ilce.il.slug diyebilmemiz lazım ama async session'da eager load gerekir.
        # Basitlik için veriyi çekerken join ile ili de almıştık (session ayarına göre değişir).
        # Garanti olsun diye tekrar il bilgisini çekiyoruz (Performans optimizasyonu sonra yapılabilir)
        
        il_stmt = select(models.Il).where(models.Il.id == ilce.il_id)
        il_result = await db.execute(il_stmt)
        il = il_result.scalar_one()

        url = f"https://www.eczaneler.gen.tr/nobetci-{il.slug}-{ilce.slug}"
        
        try:
            # Requests senkron çalışır, burada basit tutuyoruz.
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Tablo yapısını bul (Senin kodun aynısı)
                active_div = soup.find("div", {"class": "tab-content"}).find("div", {"class": "active"})
                
                if active_div:
                    table = active_div.find("table")
                    if table:
                        thead = table.find("thead", class_="thead-dark")
                        if thead:
                            rows = thead.find_next_siblings("tr")
                            
                            for tr in rows:
                                try:
                                    eczane_ad = tr.find("div", {"class": "col-lg-3"}).get_text(strip=True)
                                    
                                    # --- GÜNCELLENEN KISIM (ADRES TEMİZLİĞİ) ---
                                    adres_container = tr.find("div", {"class": "col-lg-6"})
                                    
                                    if adres_container:
                                        # 1. Adım: Tarif kısmını sil (py-2)
                                        # find_all kullanıyoruz çünkü bazen birden fazla olabilir, garanti olsun.
                                        for unwanted in adres_container.find_all("div", class_="py-2"):
                                            unwanted.decompose() # Elemanı HTML ağacından tamamen siler
                                        
                                        # 2. Adım: Mahalle etiketini sil (my-2)
                                        for unwanted in adres_container.find_all("div", class_="my-2"):
                                            unwanted.decompose()

                                        # 3. Adım: Artık içerideki çöp divler silindi, kalan saf metni al
                                        eczane_adres = adres_container.get_text(strip=True)
                                    else:
                                        eczane_adres = ""
                                    # --- GÜNCELLENEN KISIM BİTİŞ ---

                                    eczane_telefon = tr.find("div", {"class": "py-lg-2"}).get_text(strip=True)
                                    
                                    # DB'ye Ekleme kodu aynen devam...
                                    new_eczane = models.Eczane(
                                        il_id=il.id,
                                        ilce_id=ilce.id,
                                        eczane_adi=eczane_ad,
                                        adres=eczane_adres,
                                        telefon=eczane_telefon
                                    )
                                    db.add(new_eczane)

                                except AttributeError:
                                    continue
                            
                            # Her ilçe bitiminde commit yapalım
                            await db.commit()
            
        except Exception as e:
            print(f"Hata ({ilce.slug}): {e}")

        # İlerleme Bilgisi Gönder
        processed_count += 1
        percentage = int((processed_count / total_count) * 100)
        
        # Frontend'e log formatında veri gönderiyoruz
        # Format: PROGRESS|Yüzde|Mesaj
        yield f"PROGRESS|{percentage}|{il.baslik}/{ilce.baslik} tarandı...\n"

    yield "PROGRESS|100|İşlem Tamamlandı!"