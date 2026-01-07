# Nöbetçi Eczane - Frontend

Modern, mobile-first Nuxt 3 application for finding duty pharmacies.

## Tech Stack

- **Framework:** Nuxt 3 (SSR enabled)
- **Language:** TypeScript (Strict mode)
- **Styling:** Tailwind CSS + Nuxt UI
- **State Management:** Pinia with persisted state
- **Icons:** Lucide Vue Next
- **Package Manager:** pnpm

## Features

- 🏥 Find duty pharmacies by district
- 📍 Google Maps deep linking for directions (address-based)
- 📞 Direct call functionality
- ⭐ Favorite district persistence
- 📱 Mobile-first, responsive design
- ⚡ Fast, optimized performance
- 🎨 Modern, clean UI with smooth animations

## Setup

### Prerequisites

- Node.js 18+
- pnpm (install with `npm install -g pnpm`)
- Backend API running on `http://127.0.0.1:8000`

### Installation

```bash
# Install dependencies
pnpm install

# Copy environment file
cp .env.example .env

# Start development server
pnpm run dev
```

The application will be available at `http://localhost:3000`

## Environment Variables

Create a `.env` file in the root directory:

```env
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000
```

## Project Structure

```
frontend/
├── app/
│   └── app.vue              # Main application component
├── components/
│   ├── AppHeader.vue        # Header with branding
│   ├── DistrictSelector.vue # City/District selector
│   └── PharmacyCard.vue     # Pharmacy display card
├── composables/
│   └── useApi.ts            # API integration
├── stores/
│   └── pharmacy.ts          # Pinia store for state
├── types/
│   └── index.ts             # TypeScript definitions
├── utils/
│   └── maps.ts              # Google Maps utilities
└── nuxt.config.ts           # Nuxt configuration
```

## API Integration

The frontend connects to the FastAPI backend with these endpoints:

- `GET /iller/` - List all cities
- `GET /iller/{il_id}/ilceler` - List districts by city
- `GET /eczaneler/` - List all pharmacies

## Building for Production

```bash
# Build the application
pnpm run build

# Preview production build
pnpm run preview
```

## Development Notes

- The application uses **address-based** Google Maps deep linking (no coordinates in backend)
- State is persisted in localStorage for favorite districts
- All components use Vue 3 Composition API with `<script setup>`
- TypeScript strict mode is enabled for type safety
- Mobile-first design with 44px minimum touch targets

## License

MIT
