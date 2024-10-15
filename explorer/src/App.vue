<template>
  <Suspense>
    <template #default>
      <MainScreen />
    </template>
    <template #fallback>
      <div class="flex items-center justify-center h-screen">
        <div class="spinner">Loading...</div>
      </div>
    </template>
  </Suspense>
</template>

<script lang="ts" setup>
import MainScreen from "./components/MainScreen.vue";
</script>
