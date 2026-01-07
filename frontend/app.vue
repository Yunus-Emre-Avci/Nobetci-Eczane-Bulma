<template>
  <UApp>
    <div
      class="min-h-screen bg-[#f8fafc] dark:bg-[#0f172a] text-[#1e293b] dark:text-[#f1f5f9] font-sans transition-colors duration-500 pb-20"
    >
      <!-- Super Simple Header -->
      <header
        class="sticky top-0 z-50 bg-white/80 dark:bg-[#1e293b]/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800"
      >
        <div
          class="container mx-auto px-4 py-4 flex items-center justify-between"
        >
          <!-- Big Logo-Like Branding -->
          <div
            class="flex items-center gap-3 cursor-pointer"
            @click="selectedDistrictId = null"
          >
            <div
              class="w-10 h-10 md:w-12 md:h-12 bg-rose-500 rounded-2xl flex items-center justify-center shadow-lg shadow-rose-500/10"
            >
              <Icon
                name="i-heroicons-plus-16-solid"
                class="w-6 h-6 md:w-8 md:h-8 text-white"
              />
            </div>
            <div class="flex flex-col">
              <span
                class="text-xl md:text-2xl font-black tracking-tight text-rose-600 dark:text-rose-400"
                >ECZANE BUL</span
              >
              <span
                class="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-widest mt-0.5"
                >İSTANBUL REHBERİ</span
              >
            </div>
          </div>

          <!-- Obvious Night/Day Switcher -->
          <div class="flex items-center gap-2">
            <button
              @click="toggleColorMode"
              class="flex items-center gap-2 px-4 py-2 rounded-full bg-slate-100 dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 hover:border-rose-300 dark:hover:border-rose-700 transition-all font-bold text-sm"
            >
              <Icon
                :name="
                  colorMode.value === 'dark'
                    ? 'i-heroicons-sun-solid'
                    : 'i-heroicons-moon-solid'
                "
                class="w-5 h-5 text-rose-500"
              />
              <span class="hidden sm:inline">{{
                colorMode.value === "dark" ? "Gündüz Modu" : "Gece Modu"
              }}</span>
              <span class="sm:hidden">{{
                colorMode.value === "dark" ? "Gündüz" : "Gece"
              }}</span>
            </button>
          </div>
        </div>
      </header>

      <main class="container mx-auto px-4 py-8 max-w-4xl">
        <!-- 1. SEARCH/DISTRICTS -->
        <div
          v-if="!selectedDistrictId"
          class="space-y-12 animate-in fade-in slide-in-from-bottom-4 duration-500"
        >
          <!-- Large, Friendly Search -->
          <div class="text-center space-y-6">
            <div class="space-y-2">
              <h2
                class="text-3xl md:text-4xl font-extrabold text-slate-800 dark:text-white"
              >
                Size En Yakın <span class="text-rose-500">Nöbetçi</span> Eczane
              </h2>
              <p
                class="text-lg text-slate-500 dark:text-slate-400 font-medium max-w-lg mx-auto leading-tight"
              >
                Görmek istediğiniz bölgeyi arayın veya aşağıdan üzerine
                tıklayın.
              </p>
            </div>

            <div class="relative max-w-xl mx-auto group">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Örn: Kadıköy, Kartal..."
                class="w-full pl-6 pr-14 py-5 bg-white dark:bg-slate-900 border-3 border-slate-100 dark:border-slate-800 rounded-3xl text-xl font-bold shadow-xl shadow-slate-200/50 dark:shadow-none focus:border-rose-400 dark:focus:border-rose-600 outline-none transition-all placeholder:text-slate-300"
              />
              <div
                class="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-rose-500 rounded-xl flex items-center justify-center text-white"
              >
                <Icon
                  name="i-heroicons-magnifying-glass-16-solid"
                  class="w-6 h-6"
                />
              </div>
            </div>
          </div>

          <!-- Favorites - Simplified -->
          <section
            v-if="favoriteDistricts.length > 0 && !searchQuery"
            class="space-y-4"
          >
            <h3
              class="flex items-center gap-2 text-xs font-black text-rose-500 uppercase tracking-widest px-1"
            >
              <Icon name="i-heroicons-star-solid" class="w-4 h-4" />
              HIZLI ERİŞİM (FAVORİLER)
            </h3>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div
                v-for="district in favoriteDistricts"
                :key="'fav-' + district.id"
                class="group relative"
              >
                <button
                  @click="selectDistrict(district.id)"
                  class="w-full bg-white dark:bg-slate-900 rounded-2xl p-4 shadow-sm border-2 border-rose-100 dark:border-rose-900/30 hover:border-rose-400 transition-all active:scale-95 flex flex-col items-center gap-1"
                >
                  <span class="font-bold text-slate-800 dark:text-white">{{
                    district.baslik
                  }}</span>
                  <span class="text-[10px] text-rose-500 font-black uppercase"
                    >GİT</span
                  >
                </button>
                <button
                  @click.stop="store.toggleFavorite(district.id)"
                  class="absolute -top-2 -right-2 w-7 h-7 bg-slate-800 text-white rounded-full flex items-center justify-center shadow-lg"
                  title="Sil"
                >
                  <Icon name="i-heroicons-x-mark" class="w-4 h-4" />
                </button>
              </div>
            </div>
          </section>

          <!-- Main Grid -->
          <section class="space-y-4">
            <h3
              class="flex items-center gap-2 text-xs font-black text-slate-400 dark:text-slate-600 uppercase tracking-widest px-1"
            >
              <Icon name="i-heroicons-map-pin-solid" class="w-4 h-4" />
              TÜM BÖLGELER (A-Z)
            </h3>
            <div
              v-if="loadingDistricts"
              class="grid grid-cols-2 sm:grid-cols-4 gap-3"
            >
              <USkeleton v-for="i in 8" :key="i" class="h-20 rounded-2xl" />
            </div>
            <div v-else class="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <div
                v-for="district in filteredSortedDistricts"
                :key="district.id"
                class="group relative"
              >
                <button
                  @click="selectDistrict(district.id)"
                  class="w-full h-full bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 hover:border-rose-400 hover:shadow-lg transition-all active:scale-95 text-center font-bold text-slate-700 dark:text-slate-300"
                >
                  {{ district.baslik }}
                </button>
                <button
                  @click.stop="store.toggleFavorite(district.id)"
                  class="absolute top-2 right-2 p-1.5 rounded-full transition-colors"
                  :class="[
                    store.isFavorite(district.id)
                      ? 'text-rose-500'
                      : 'text-slate-200 hover:text-rose-300 dark:text-slate-700',
                  ]"
                  :disabled="
                    !store.isFavorite(district.id) &&
                    !store.canAddMoreFavorites()
                  "
                >
                  <Icon name="i-heroicons-star-solid" class="w-5 h-5" />
                </button>
              </div>
            </div>
          </section>
        </div>

        <!-- 2. PHARMACY LIST -->
        <div
          v-else
          class="space-y-6 animate-in slide-in-from-right-4 duration-400"
        >
          <!-- Back Bar -->
          <div
            class="flex items-center gap-4 bg-white dark:bg-slate-900 p-4 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm"
          >
            <button
              @click="selectedDistrictId = null"
              class="flex items-center gap-2 px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-xl font-black text-sm hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            >
              <Icon name="i-heroicons-chevron-left-solid" class="w-5 h-5" />
              GERİ GİT
            </button>
            <div class="flex-1">
              <h2
                class="text-xl font-bold uppercase tracking-tight text-slate-800 dark:text-white"
              >
                {{ selectedDistrictName }}
              </h2>
            </div>
            <button
              @click="store.toggleFavorite(selectedDistrictId!)"
              class="p-2 rounded-xl transition-colors"
              :class="[store.isFavorite(selectedDistrictId!) ? 'bg-rose-100 text-rose-500' : 'bg-slate-50 text-slate-300 dark:bg-slate-800']"
            >
              <Icon
                :name="store.isFavorite(selectedDistrictId!) ? 'i-heroicons-star-solid' : 'i-heroicons-star'"
                class="w-6 h-6"
              />
            </button>
          </div>

          <!-- Loading Pharmacies -->
          <div v-if="loadingPharmacies" class="space-y-4">
            <USkeleton v-for="i in 3" :key="i" class="h-44 rounded-3xl" />
          </div>

          <div v-else-if="filteredPharmacies.length > 0" class="space-y-4">
            <!-- Uyarı Notu -->
            <div
              class="bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-950/20 dark:to-orange-950/20 border-2 border-amber-200 dark:border-amber-800/40 rounded-2xl p-5 shadow-sm"
            >
              <div class="flex items-start gap-4">
                <div
                  class="flex-shrink-0 w-10 h-10 bg-amber-500 rounded-xl flex items-center justify-center"
                >
                  <Icon
                    name="i-heroicons-exclamation-triangle-16-solid"
                    class="w-6 h-6 text-white"
                  />
                </div>
                <div class="flex-1 space-y-1">
                  <h4
                    class="text-sm font-black text-amber-900 dark:text-amber-400 uppercase tracking-wide"
                  >
                    ÖNEMLİ BİLGİLENDİRME
                  </h4>
                  <p
                    class="text-sm text-amber-800 dark:text-amber-300 leading-relaxed font-medium"
                  >
                    Eczanelerin nöbet koşullarında istisnai durumlar
                    yaşanabilmektedir. Herhangi bir mağduriyet yaşamamanız
                    adına, ilgili eczaneye gitmeden önce telefonla iletişime
                    geçerek açık olup olmadıklarını teyit etmeniz önemle tavsiye
                    edilir.
                  </p>
                </div>
              </div>
            </div>

            <TransitionGroup name="list" tag="div" class="space-y-4">
              <PharmacyCard
                v-for="pharmacy in filteredPharmacies"
                :key="pharmacy.id"
                :pharmacy="pharmacy"
              />
            </TransitionGroup>
          </div>

          <!-- Empty Screen -->
          <div
            v-else
            class="text-center py-20 bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800"
          >
            <Icon
              name="i-heroicons-information-circle"
              class="w-16 h-16 text-slate-200 mx-auto mb-4"
            />
            <h3 class="text-xl font-bold text-slate-800 dark:text-white">
              ECZANE BULUNAMADI
            </h3>
            <p class="text-slate-500 max-w-xs mx-auto mt-2">
              Bu bölge için aktif bir nöbet listesi henüz eklenmemiş olabilir.
            </p>
          </div>
        </div>
      </main>

      <!-- Bottom Quick Bar for Mobile -->
      <footer
        v-if="selectedDistrictId"
        class="sm:hidden fixed bottom-6 left-0 right-0 px-4 z-50"
      >
        <button
          @click="selectedDistrictId = null"
          class="w-full bg-slate-900 dark:bg-rose-600 text-white py-4 rounded-2xl font-black shadow-2xl flex items-center justify-center gap-2 active:scale-95 transition-all"
        >
          <Icon name="i-heroicons-arrow-path" class="w-5 h-5" />
          DİĞER BÖLGELERE BAK
        </button>
      </footer>
    </div>
  </UApp>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import type { EczaneResponse } from "~/types";
import { usePharmacyStore } from "~/stores/pharmacy";

const { fetchIstanbulDistricts, fetchEczaneler } = useApi();
const store = usePharmacyStore();
const colorMode = useColorMode();

const toggleColorMode = () => {
  colorMode.preference = colorMode.value === "dark" ? "light" : "dark";
};

// State
const selectedDistrictId = ref<number | null>(null);
const currentTime = ref("");
const searchQuery = ref("");

// Data
const { data: districtsData, pending: loadingDistricts } =
  fetchIstanbulDistricts();
const { data: allPharmacies, pending: loadingPharmacies } = fetchEczaneler();

// Computeds
const sortedDistricts = computed(() => {
  if (!districtsData.value) return [];
  return [...districtsData.value].sort((a, b) =>
    a.baslik.localeCompare(b.baslik, "tr")
  );
});

const filteredSortedDistricts = computed(() => {
  if (!searchQuery.value) return sortedDistricts.value;
  const q = searchQuery.value.toLowerCase().trim();
  return sortedDistricts.value.filter((d) =>
    d.baslik.toLowerCase().includes(q)
  );
});

const favoriteDistricts = computed(() => {
  if (!districtsData.value) return [];
  return districtsData.value
    .filter((d) => store.favoriteDistrictIds.includes(d.id))
    .sort((a, b) => a.baslik.localeCompare(b.baslik, "tr"));
});

const selectedDistrictName = computed(() => {
  if (!selectedDistrictId.value || !districtsData.value) return "";
  const district = districtsData.value.find(
    (d) => d.id === selectedDistrictId.value
  );
  return district?.baslik || "";
});

const filteredPharmacies = computed<EczaneResponse[]>(() => {
  if (!selectedDistrictId.value || !allPharmacies.value) return [];
  return allPharmacies.value.filter(
    (p) => p.ilce_id === selectedDistrictId.value
  );
});

// Actions
const selectDistrict = (districtId: number) => {
  selectedDistrictId.value = districtId;
  searchQuery.value = "";
  window.scrollTo({ top: 0, behavior: "smooth" });
};

const updateTime = () => {
  const now = new Date();
  currentTime.value = now.toLocaleTimeString("tr-TR", {
    hour: "2-digit",
    minute: "2-digit",
  });
};

onMounted(() => {
  updateTime();
  setInterval(updateTime, 60000);
});
</script>

<style scoped>
.list-enter-active {
  transition: all 0.4s ease-out;
}
.list-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.list-move {
  transition: transform 0.4s ease;
}

@font-face {
  font-family: "Inter";
  src: url("https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap");
}
body {
  font-family: "Inter", sans-serif;
}
</style>
