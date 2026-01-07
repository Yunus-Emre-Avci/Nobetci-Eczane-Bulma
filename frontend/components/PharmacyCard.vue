<template>
  <div
    class="relative group bg-white dark:bg-slate-900 rounded-3xl p-6 md:p-8 shadow-sm hover:shadow-xl border border-slate-100 dark:border-slate-800 transition-all duration-300 overflow-hidden"
  >
    <div class="flex flex-col lg:flex-row gap-8 lg:items-center relative z-10">
      <!-- Info Zone -->
      <div class="flex-1 space-y-6">
        <div class="flex items-center gap-4">
          <div
            class="w-12 h-12 bg-rose-50 dark:bg-rose-900/20 rounded-2xl flex items-center justify-center text-rose-500"
          >
            <Icon
              name="i-heroicons-building-storefront-16-solid"
              class="w-7 h-7"
            />
          </div>
          <div>
            <h3
              class="text-xl md:text-2xl font-black text-slate-800 dark:text-white leading-tight uppercase tracking-tight"
            >
              {{ pharmacy.eczane_adi }}
            </h3>
            <div class="flex items-center gap-2 mt-1">
              <span class="inline-flex h-2 w-2 rounded-full bg-rose-500"></span>
              <span
                class="text-[10px] font-black text-rose-500 uppercase tracking-widest"
                >Nöbetçi Eczane</span
              >
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div
            class="flex items-start gap-3 bg-slate-50 dark:bg-slate-800/40 p-4 rounded-2xl border border-slate-100 dark:border-slate-800 transition-colors"
          >
            <Icon
              name="i-heroicons-map-pin-16-solid"
              class="w-5 h-5 text-slate-400 mt-0.5 flex-shrink-0"
            />
            <p
              class="text-sm text-slate-600 dark:text-slate-400 font-semibold leading-snug"
            >
              {{ pharmacy.adres }}
            </p>
          </div>
          <div
            v-if="pharmacy.telefon"
            class="flex items-center gap-3 bg-rose-50/50 dark:bg-rose-950/20 p-4 rounded-2xl border border-rose-100 dark:border-rose-900/30 transition-colors"
          >
            <Icon
              name="i-heroicons-phone-16-solid"
              class="w-5 h-5 text-rose-400 flex-shrink-0"
            />
            <div class="flex flex-col">
              <span
                class="text-[10px] font-black text-slate-400 uppercase tracking-widest"
                >Telefon</span
              >
              <p
                class="text-lg text-slate-700 dark:text-slate-300 font-black tracking-tight"
              >
                {{ formatPhone(pharmacy.telefon) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Zone -->
      <div class="flex flex-col sm:flex-row lg:flex-col gap-3 min-w-[240px]">
        <a
          :href="mapsLink"
          target="_blank"
          class="flex-1 flex items-center justify-center gap-3 px-8 py-4 bg-rose-500 hover:bg-rose-600 dark:bg-rose-600 dark:hover:bg-rose-500 text-white rounded-2xl font-black text-lg transition-all active:scale-95 shadow-lg shadow-rose-500/20 group/btn"
        >
          <Icon name="i-heroicons-map-16-solid" class="w-6 h-6" />
          YOL TARİFİ
        </a>

        <a
          v-if="phoneLink"
          :href="phoneLink"
          class="flex-1 flex items-center justify-center gap-3 px-8 py-4 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-rose-500 border-2 border-rose-500/20 hover:border-rose-500 dark:border-rose-500/10 rounded-2xl font-black text-lg transition-all active:scale-95"
        >
          <Icon name="i-heroicons-phone-16-solid" class="w-6 h-6" />
          ARA
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import type { Eczane } from "~/types";
import { getGoogleMapsLink, getPhoneLink, formatPhone } from "~/utils/maps";

const props = defineProps<{
  pharmacy: Eczane;
}>();

const mapsLink = computed(() => getGoogleMapsLink(props.pharmacy));
const phoneLink = computed(() => getPhoneLink(props.pharmacy.telefon));
</script>
