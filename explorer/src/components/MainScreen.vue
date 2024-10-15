<template>
  <div class="min-h-screen bg-gray-100 text-gray-900">
    <header class="bg-white shadow flex justify-between">
      <div class="max-w-7xl py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">Intelligent Oracles</h1>
      </div>
      <div class="max-w-7xl py-6 px-4 sm:px-6 lg:px-8 text-right">
        <div v-if="!userAddress">
          <button
            @click="createUserAccount"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Create Account
          </button>
        </div>
        <div v-else>
          <p class="text-lg">Your address: <Address :address="userAddress" /></p>
        </div>
      </div>
    </header>
    <main class="mx-auto py-6 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <!-- Oracle Cards -->
        <div v-for="oracle in oracles" :key="oracle.id" class="bg-white shadow rounded-lg overflow-hidden">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900 mb-2">{{ oracle.title }}</h3>
            <p class="text-sm text-gray-500 mb-4">
              <Address :address="oracle.address" />
            </p>
            <div class="mb-4">
              <h4 class="text-sm font-medium text-gray-500">Potential Outcomes:</h4>
              <p class="text-sm text-gray-900">{{ oracle.potential_outcomes.join(', ') }}</p>
            </div>
            <div class="mb-4">
              <h4 class="text-sm font-medium text-gray-500">Rules:</h4>
              <p class="text-sm text-gray-900">{{ oracle.rules.join(', ') }}</p>
            </div>
            <div class="mb-4">
              <h4 class="text-sm font-medium text-gray-500">Status:</h4>
              <span :class="oracle.status === 'Active' ? 'text-green-600' : 'text-yellow-600'">
                {{ oracle.status }}
              </span>
            </div>
            <div class="mb-4">
              <h4 class="text-sm font-medium text-gray-500">Outcome:</h4>
              <p class="text-sm text-gray-900">{{ oracle.outcome || 'Not yet determined' }}</p>
            </div>
            <div class="mt-4">
              <button
                v-if="oracle.creator === userAddress && oracle.status === 'Active'"
                @click="resolvePrediction(oracle.id)"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Resolve
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>

</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { account, createAccount, client } from "../services/genlayer";
import Address from "./Address.vue";
// State
const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS;
const userAccount = ref(account);
const userAddress = computed(() => userAccount.value?.address);
const oracles = ref([]);
const leaderboard = ref([]);


// Load data from the backend
// TODO: it might be a good idea to use a store for this
onMounted(async () => {
  const contract_addresses = await client.readContract({
    address: contractAddress,
    functionName: "get_contract_addresses",
    args: [],
  });
  console.log(contract_addresses);
  oracles.value = await Promise.all(contract_addresses.map((address) => client.readContract(
    {
      address,
      functionName: "get_dict",
      args: [],
    }
  ).then(result => ({ ...result, address }))));
  console.log(oracles.value);

  // Clone the oracles value 5 times for testing purposes
  oracles.value = Array(5).fill().map(() => [...oracles.value]).flat();
  console.log("Cloned oracles:", oracles.value);
});
//   {
//   "analysis": null,
//   "creator": "0x8082FBFD1dBa92be0523a1FC0BfDf2116fD4e399",
//   "data_sources": [],
//   "description": "A market test",
//   "earliest_resolution_date": "2024-01-01T00:00:00+00:00",
//   "outcome": null,
//   "potential_outcomes": [
//     "Bayern Munich",
//     "Arsenal"
//   ],
//   "prediction_market_id": "1",
//   "rules": [
//     "The outcome is the winner of the match"
//   ],
//   "status": "Active",
//   "title": "Football Prediction Market",
//   "valid_data_sources": [
//     "bbc"
//   ]
// }
</script>
