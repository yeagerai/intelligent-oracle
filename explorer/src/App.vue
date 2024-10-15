<template>
  <Suspense>
    <template #default>
      <PredictionMarketScreen />
    </template>
    <template #fallback>
      <div class="flex items-center justify-center h-screen">
        <div class="spinner">Loading...</div>
      </div>
    </template>
  </Suspense>
</template>

<script lang="ts" setup>
import PredictionMarketScreen from "./components/PredictionMarketScreen.vue";
</script>
