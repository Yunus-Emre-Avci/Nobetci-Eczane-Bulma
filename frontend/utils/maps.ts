import type { Eczane } from "~/types";

/**
 * Generates a Google Maps deep link for a pharmacy
 * Since we don't have coordinates, we use address-based search
 */
export function getGoogleMapsLink(pharmacy: Eczane): string {
  // Construct full address with district and city info if available
  let searchQuery = pharmacy.adres;

  if (pharmacy.ilce?.baslik) {
    searchQuery += `, ${pharmacy.ilce.baslik}`;
  }

  if (pharmacy.il?.baslik) {
    searchQuery += `, ${pharmacy.il.baslik}`;
  }

  // Encode the address for URL
  const encodedAddress = encodeURIComponent(searchQuery);

  // Return Google Maps directions URL
  // By not providing an origin, Google Maps defaults to current location
  return `https://www.google.com/maps/dir/?api=1&destination=${encodedAddress}`;
}

/**
 * Formats phone number for tel: link
 */
export function getPhoneLink(phone: string | null): string | null {
  if (!phone) return null;
  // Remove all non-digit characters
  const cleaned = phone.replace(/\D/g, "");
  return `tel:${cleaned}`;
}

/**
 * Formats phone number for display
 */
export function formatPhone(phone: string | null): string {
  if (!phone) return "Telefon yok";
  return phone;
}
