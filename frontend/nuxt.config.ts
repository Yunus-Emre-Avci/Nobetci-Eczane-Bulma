// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",

  modules: ["@pinia/nuxt", "@pinia-plugin-persistedstate/nuxt", "@nuxt/ui"],
  css: ["~/assets/css/main.css"],
  // Disable dev tools for better performance
  devtools: { enabled: false },

  // TypeScript config - disable type checking for faster builds
  typescript: {
    strict: true,
    typeCheck: false,
    shim: false,
  },

  // Runtime config
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://127.0.0.1:8000",
    },
  },

  // App config
  app: {
    head: {
      title: "Nöbetçi Eczane",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        { name: "description", content: "Nöbetçi eczaneleri kolayca bulun" },
      ],
    },
  },

  // Vite optimization for faster HMR
  vite: {
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            "vue-vendor": ["vue", "vue-router"],
            "pinia-vendor": ["pinia"],
          },
        },
      },
    },
    optimizeDeps: {
      include: ["lucide-vue-next"],
    },
  },
});
