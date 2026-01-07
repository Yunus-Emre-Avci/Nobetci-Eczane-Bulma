# 🚑 İstanbul Nöbetçi Eczane Rehberi

İstanbul genelindeki tüm ilçelerde aktif nöbetçi eczaneleri anlık olarak listeleyen, modern araayüze sahip ve kullanıcı dostu bir web uygulamasıdır. Profesyonel, göz yormayan ve "en basit kullanıcı" seviyesinde optimize edilmiş bir UX sunar.

![Hero Banner](./docs/project_hero_banner.png)

## ✨ Öne Çıkan Özellikler

- 🔍 **Akıllı Arama:** Yazmaya başladığınız anda ilçeleri filtreleyen modern arama çubuğu.
- ⭐ **Favori Sistemi:** Sık kullandığınız 5 ilçeye kadar favori ekleme ve ana sayfadan hızlı erişim.
- 🌓 **Gece/Gündüz Modu:** Göz yorgunluğunu önleyen, net yazılarla desteklenmiş tema desteği.
- 📍 **Tek Tıkla Navigasyon:** Google Haritalar üzerinden anlık konumunuzdan eczaneye direkt rota oluşturma.
- 📱 **Tam Responsive:** Telefon, tablet ve masaüstü cihazlar için %100 uyumlu arayüz.
- 💾 **Kalıcı Veri:** Favori bölgeleriniz tarayıcı hafızasında (localStorage) güvenle saklanır.

## 🛠️ Kullanılan Teknolojiler

### Frontend

- **Framework:** Nuxt 3 (Vue.js)
- **UI Kit:** Nuxt UI & Tailwind CSS
- **State Management:** Pinia (PersistedState desteğiyle)
- **Icons:** Heroicons
- **Styling:** Headless UI & Modern CSS

### Backend

- **Core:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (Async)
- **Scraping:** BeautifulSoup4 & Requests
- **Config:** Pydantic Settings (.env desteği)

## 📁 Proje Yapısı

```text
├── backend/            # FastAPI Sunucu Kodları
│   ├── main.py         # API Endpoint'leri
│   ├── scraper.py      # Veri çekme motoru
│   ├── models.py       # DB Tablo tanımları
│   └── database.py     # DB Bağlantı ayarları
├── frontend/           # Nuxt 3 Uygulaması
│   ├── app.vue         # Ana uygulama UI
│   ├── layouts/        # Sayfa düzenleri
│   ├── components/     # Tekrar kullanılabilir parçalar
│   └── stores/         # Eczane ve Favori stateleri
└── .gitignore          # Git tarafından yoksayılacak dosyalar
```

## 🚀 Kurulum ve Çalıştırma

### 1. Backend Kurulumu

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate
pip install -r requirements.txt
```

`.env` dosyasını oluşturun:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
CORS_ORIGINS=http://localhost:3000
```

Sunucuyu başlatın:

```bash
uvicorn main:app --reload
```

### 2. Frontend Kurulumu

```bash
cd frontend
pnpm install  # veya npm install
```

`.env` dosyasını oluşturun:

```env
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000
```

Uygulamayı başlatın:

```bash
pnpm dev --open
```

## 📸 Ekran Görüntüleri

|                Ana Sayfa (Light)                 |                Ana Sayfa (Dark)                |
| :----------------------------------------------: | :--------------------------------------------: |
| ![Light Mode](./docs/screenshots/home_light.png) | ![Dark Mode](./docs/screenshots/home_dark.png) |

|               İlçe Detay Listesi               |              Hızlı Favori Yönetimi              |
| :--------------------------------------------: | :---------------------------------------------: |
| ![List View](./docs/screenshots/list_view.png) | ![Favorites](./docs/screenshots/fav_manage.png) |

---

_Geliştirici: [Antigravity AI]_
