// Type definitions matching the backend Pydantic models

export interface Il {
  id: number;
  baslik: string;
  slug: string;
}

export interface Ilce {
  id: number;
  baslik: string;
  slug: string;
  il_id: number;
}

export interface Eczane {
  id: number;
  eczane_adi: string;
  adres: string;
  telefon: string | null;
  il_id: number;
  ilce_id: number;
  olusturulma_tarihi: string;
  il?: Il;
  ilce?: Ilce;
}

// API Response types
export type IlResponse = Il;
export type IlceResponse = Ilce;
export type EczaneResponse = Eczane;
