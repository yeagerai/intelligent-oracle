<template>
  <div class="min-h-screen text-primary-text">
    <header class="bg-white shadow flex justify-between items-center pt-16">
      <div class="max-w-7xl mx-auto flex justify-between items-center w-full">
        <div class="py-6 sm:px-4">
          <h1 class="text-3xl font-bold text-primary-text">Intelligent Oracle Explorer</h1>
        </div>
        <button @click="refreshOracles" class="mr-4 px-4 py-2 bg-highlight text-white rounded hover:opacity-80 transition-colors">
          Refresh
        </button>
      </div>
    </header>
    <main class="mx-auto py-6 sm:px-6 lg:px-8 max-w-7xl px-4">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Oracle Cards -->
        <router-link
          v-for="oracle in [...oracles].reverse()"
          :key="oracle.address"
          :to="{ name: 'OracleDetails', params: { address: oracle.address } }"
          class="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300"
        >
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-primary-text mb-2">{{ oracle.title }}</h3>

            <p class="text-sm text-secondary-text mb-2">
              <Address :address="oracle.address" />
            </p>

            
              <span :class="{
                'mb-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium': true,
                'bg-highlight/20 text-highlight': oracle.status === 'Active',
                'bg-green-100 text-green-800': oracle.status === 'Resolved',
                'bg-red-100 text-red-800': oracle.status === 'Error'
                }">
                  {{ oracle.status }}
              </span>
            
            
            
            <div class="mb-2">
              <h4 class="text-sm font-medium text-secondary-text">Description:</h4>
              <p class="text-sm text-primary-text">{{ oracle.description }}</p>
            </div>
            <div class="mb-2" v-if="oracle.outcome">
              <h4 class="text-sm font-medium text-secondary-text">Outcome:</h4>
              <p class="text-sm text-primary-text">{{ oracle.outcome || 'Not yet determined' }}</p>
            </div>
          </div>
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { Oracle, useGenlayerStore } from "../stores/genlayerStore"; 
import Address from "./Address.vue";
import { onBeforeRouteUpdate } from 'vue-router';

const genlayerStore = useGenlayerStore();
const oracles = ref<Oracle[]>([]);

onMounted(async () => {
  loadOracles();
  refreshOracles();
});

async function loadOracles() {
  oracles.value = await genlayerStore.oracles;
}

// Add refresh function
async function refreshOracles() {
  await genlayerStore.refreshOracles();
  await loadOracles();
}

// Helper function to format date
const formatDate = (dateString: string) => {
  if (!dateString) return 'Not specified';
  const date = new Date(dateString);
  return date.toLocaleString();
};

</script>
