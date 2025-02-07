<template>
  <AppHeader :chatUrl="chatUrl" />
  <router-view></router-view>
</template>

<script setup>
import AppHeader from "./components/AppHeader.vue";
const chatUrl = import.meta.env.VITE_CHAT_URL;
// No additional setup needed here
</script>
