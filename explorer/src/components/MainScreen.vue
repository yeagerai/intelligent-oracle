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
          <p class="text-lg">Your points: {{ userPoints }}</p>
        </div>
      </div>
    </header>
    <main class="mx-auto py-6 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 md:grid-cols-10 gap-8">
        <!-- Predictions List -->
        <div class="bg-white shadow overflow-hidden sm:rounded-lg col-span-7">
          <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
            <h2 class="text-lg leading-6 font-medium text-gray-900">Oracles</h2>
            <button
              @click="openCreateModal"
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded text-sm"
            >
              Create Prediction
            </button>
          </div>
          <div class="border-t border-gray-200">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    User
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Game Date
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Team 1
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Team 2
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Predicted Winner
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Status
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Result
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Action
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="oracle in oracles" :key="oracle.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <Address :address="oracle.address" />
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ oracle.game_date }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ oracle.team1 }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ oracle.team2 }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ oracle.predicted_winner === "0" ? "Draw" : (oracle.predicted_winner === "1" ? oracle.team1 : oracle.team2) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span :class="oracle.has_resolved ? 'text-green-600' : 'text-yellow-600'">
                      {{ oracle.has_resolved ? "Resolved" : "Unresolved" }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span v-if="oracle.has_resolved" :class="oracle.predicted_winner === String(oracle.real_winner) ? 'text-green-600' : 'text-red-600'">
                      {{ oracle.predicted_winner === String(oracle.real_winner) ? "Success" : "Failure" }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div v-if="resolvingPrediction !== oracle.id">
                      <button
                        v-if="oracle.owner === userAddress && !oracle.has_resolved"
                        @click="resolvePrediction(oracle.id)"
                        class="text-indigo-600 hover:text-indigo-900"
                      >
                        Resolve
                      </button>
                    </div>
                    <div v-else>Resolving prediction</div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Leaderboard -->
        <div class="bg-white shadow overflow-hidden sm:rounded-lg col-span-3">
          <div class="px-4 py-5 sm:px-6">
            <h2 class="text-lg leading-6 font-medium text-gray-900">Detail</h2>
          </div>
          <div class="border-t border-gray-200">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Rank
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Address
                  </th>
                  <th
                    scope="col"
                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Points
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(user, index) in leaderboard" :key="user.address">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ index + 1 }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <Address :address="user.address" />
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ user.points }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Create Prediction Modal -->
      <div
        v-if="showCreateModal"
        class="fixed inset-0 bg-gray-600 bg-opacity-75 overflow-y-auto h-full w-full flex items-center justify-center"
      >
        <div class="relative p-5 border w-96 shadow-lg rounded-md bg-white">
          <h3 class="text-lg font-medium leading-6 text-gray-900 mb-2">Create Prediction</h3>
          <input
            v-model="gameDate"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 mb-2"
            placeholder="Game Date (YYYY-MM-DD)"
          />
          <input
            v-model="team1"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 mb-2"
            placeholder="Team 1"
          />
          <input
            v-model="team2"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 mb-2"
            placeholder="Team 2"
          />
          <select
            v-model="predictedWinner"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 mb-2"
          >
            <option value="" disabled selected>Select Predicted Winner</option>
            <option value="0">Draw</option>
            <option value="1">Team 1</option>
            <option value="2">Team 2</option>
          </select>
          <div class="mt-4">
            <div v-if="!creatingPrediction">
              <button
                @click="createPrediction"
                class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
              >
                Create
              </button>
              <button
                @click="showCreateModal = false"
                class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
              >
                Cancel
              </button>
            </div>
            <div v-else>
              <div class="spinner">Creating...</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>

  <div class="flex items-center justify-center h-screen">
    <div class="spinner">Loading...</div>
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
});
</script>
