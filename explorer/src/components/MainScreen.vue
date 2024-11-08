<template>
  <div class="min-h-screen bg-gray-100 text-gray-900">
    <header class="bg-white shadow flex justify-between items-center">
      <div class="max-w-7xl py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">Intelligent Oracles</h1>
      </div>
      <!-- Add refresh button -->
      <button @click="refreshOracles" class="mr-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
        Refresh Oracles
      </button>
    </header>
    <main class="mx-auto py-6 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Oracle Cards -->
        <router-link
          v-for="oracle in oracles"
          :key="oracle.address"
          :to="{ name: 'OracleDetails', params: { address: oracle.address } }"
          class="bg-white shadow rounded-lg overflow-hidden hover:shadow-lg transition-shadow duration-300"
        >
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-2">{{ oracle.title }}</h3>
            <p class="text-sm text-gray-500 mb-4">
              <Address :address="oracle.address" />
            </p>
            <div class="mb-2">
              <h4 class="text-sm font-medium text-gray-500">Description:</h4>
              <p class="text-sm text-gray-900">{{ oracle.description }}</p>
            </div>
            <div class="mb-2">
              <h4 class="text-sm font-medium text-gray-500">Potential Outcomes:</h4>
              <ul class="list-disc pl-5 text-sm text-gray-900">
                <li v-for="outcome in oracle.potential_outcomes" :key="outcome">{{ outcome }}</li>
              </ul>
            </div>
            <div class="mb-2">
              <h4 class="text-sm font-medium text-gray-500">Rules:</h4>
              <ul class="list-disc pl-5 text-sm text-gray-900">
                <li v-for="rule in oracle.rules" :key="rule">{{ rule }}</li>
              </ul>
            </div>
            <div class="mb-2">
              <h4 class="text-sm font-medium text-gray-500">Status:</h4>
              <span :class="oracle.status === 'Active' ? 'text-green-600' : 'text-yellow-600'">
                {{ oracle.status }}
              </span>
            </div>
            <div class="mb-2">
              <h4 class="text-sm font-medium text-gray-500">Outcome:</h4>
              <p class="text-sm text-gray-900">{{ oracle.outcome || 'Not yet determined' }}</p>
            </div>
            <div class="mb-2">
              <h4 class="text-sm font-medium text-gray-500">Earliest Resolution Date:</h4>
              <p class="text-sm text-gray-900">{{ formatDate(oracle.earliest_resolution_date) }}</p>
            </div>
            <div class="mb-2">
              <h4 class="text-sm font-medium text-gray-500">Prediction Market ID:</h4>
              <p class="text-sm text-gray-900">{{ oracle.prediction_market_id }}</p>
            </div>
            <div class="mb-2" v-if="oracle.data_sources_domains.length > 0">
              <h4 class="text-sm font-medium text-gray-500">Data Sources Domains:</h4>
              <ul class="list-disc pl-5 text-sm text-gray-900">
                <li v-for="source in oracle.data_sources_domains" :key="source">{{ source }}</li>
              </ul>
            </div>
            <div class="mb-2" v-if="oracle.resolution_urls.length > 0">
              <h4 class="text-sm font-medium text-gray-500">Resolution URLs:</h4>
              <ul class="list-disc pl-5 text-sm text-gray-900">
                <li v-for="url in oracle.resolution_urls" :key="url">{{ url }}</li>
              </ul>
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
const genlayerStore = useGenlayerStore();
const oracles = ref<Oracle[]>([]);

onMounted(async () => {
  await loadOracles();
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
