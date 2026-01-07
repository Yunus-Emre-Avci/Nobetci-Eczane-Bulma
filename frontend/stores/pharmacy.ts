import { defineStore } from "pinia";
import { persistedState } from "#imports";

export const usePharmacyStore = defineStore("pharmacy", {
  state: () => ({
    favoriteDistrictIds: [] as number[],
  }),

  actions: {
    toggleFavorite(districtId: number) {
      const index = this.favoriteDistrictIds.indexOf(districtId);

      if (index > -1) {
        // Remove from favorites
        this.favoriteDistrictIds.splice(index, 1);
      } else {
        // Add to favorites (max 5)
        if (this.favoriteDistrictIds.length < 5) {
          this.favoriteDistrictIds.push(districtId);
        }
      }
    },

    isFavorite(districtId: number): boolean {
      return this.favoriteDistrictIds.includes(districtId);
    },

    canAddMoreFavorites(): boolean {
      return this.favoriteDistrictIds.length < 5;
    },
  },

  getters: {
    favoritesCount: (state) => state.favoriteDistrictIds.length,
    hasFavorites: (state) => state.favoriteDistrictIds.length > 0,
  },

  persist: {
    storage: persistedState.localStorage,
  },
});
