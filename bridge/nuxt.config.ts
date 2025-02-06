// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["@nuxtjs/tailwindcss"],

  nitro: {
    preset: "", // you can use 'vercel' or other providers here
  },

  runtimeConfig: {
    openaiApiKey: process.env.NUXT_OPENAI_API_KEY,
    openaiApiModel: process.env.NUXT_OPENAI_API_MODEL,
    simulatorUrl: process.env.NUXT_SIMULATOR_ENDPOINT,
    bridgePrivateKey: process.env.NUXT_BRIDGE_PRIVATE_KEY,
    icRegistryAddress: process.env.NUXT_IC_REGISTRY_ADDRESS,
  },

  compatibilityDate: "2024-07-05",

  tailwindcss: {
    configPath: "~/tailwind.config.js",
  },
});
