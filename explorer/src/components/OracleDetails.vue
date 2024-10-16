<template>
  <div class="min-h-screen bg-gray-100 text-gray-900">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-900">Oracle Details</h1>
        <div class="flex space-x-4">
          <button @click="refreshOracle" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
            Refresh Oracle
          </button>
          <router-link 
            to="/" 
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Back to Main Screen
          </router-link>
        </div>
      </div>
    </header>
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div v-if="oracle" class="flex space-x-6">
        <div class="bg-white shadow overflow-hidden sm:rounded-lg flex-1">
          <div class="px-4 py-5 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">{{ oracle.title }}</h3>
            <p class="mt-1 max-w-2xl text-sm text-gray-500">
              <Address :address="oracle.address" />
            </p>
          </div>
          <div class="border-t border-gray-200 px-4 py-5 sm:p-0">
            <dl class="sm:divide-y sm:divide-gray-200">
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Description</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ oracle.description }}</dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Potential Outcomes</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <ul class="list-disc pl-5">
                    <li v-for="outcome in oracle.potential_outcomes" :key="outcome">{{ outcome }}</li>
                  </ul>
                </dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Rules</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <ul class="list-disc pl-5">
                    <li v-for="rule in oracle.rules" :key="rule">{{ rule }}</li>
                  </ul>
                </dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Status</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <span :class="oracle.status === 'Active' ? 'text-green-600' : 'text-yellow-600'">
                    {{ oracle.status }}
                  </span>
                </dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Outcome</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ oracle.outcome || 'Not yet determined' }}</dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Earliest Resolution Date</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ formatDate(oracle.earliest_resolution_date) }}</dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Creator</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <Address :address="oracle.creator" />
                </dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Prediction Market ID</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ oracle.prediction_market_id }}</dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Valid Data Sources</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <ul class="list-disc pl-5">
                    <li v-for="source in oracle.valid_data_sources" :key="source">{{ source }}</li>
                  </ul>
                </dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Analysis</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">{{ oracle.analysis || 'No analysis available' }}</dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-gray-500">Data Sources</dt>
                <dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                  <ul class="list-disc pl-5">
                    <li v-for="source in oracle.data_sources" :key="source">{{ source }}</li>
                  </ul>
                </dd>
              </div>
            </dl>
          </div>
        </div>
        <div class="bg-white shadow overflow-hidden sm:rounded-lg flex-1">
          <div class="px-4 py-5 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">Transactions</h3>
          </div>
          <div class="border-t border-gray-200">
            <ul class="divide-y divide-gray-200">
              <li v-for="tx in transactions" :key="tx.hash" class="px-4 py-4 cursor-pointer hover:bg-gray-50" @click="openModal(tx)">
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium text-indigo-600 truncate">
                    {{ tx.hash }}
                  </p>
                  <div class="ml-2 flex-shrink-0 flex">
                    <p class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      {{ tx.status }}
                    </p>
                  </div>
                </div>
                <div class="mt-2">
                  <p class="text-sm text-gray-600">Created at: {{ formatDate(tx.created_at) }}</p>
                  <p class="text-sm text-gray-600">Nonce: {{ tx.nonce }}</p>
                  <h4 class="text-sm font-medium text-gray-900 mt-2">Validators and Votes:</h4>
                  <template v-if="tx.consensus_data.validators.length > 0">
                    <ul class="mt-1 space-y-1">
                      <li v-for="validator in tx.consensus_data.validators" :key="validator.address" class="text-sm text-gray-600">
                        {{ validator.address }}: {{ tx.consensus_data.votes[validator.address] || 'No vote' }}
                      </li>
                    </ul>
                  </template>
                  <template v-else>
                    <p class="mt-1 text-sm text-gray-600">Leader only execution</p>
                  </template>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-8">
        <p class="text-xl text-gray-600">Loading oracle details...</p>
      </div>
    </main>

    <!-- Transaction Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" @click="closeModal">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white" @click.stop>
        <div class="mt-3 text-center">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Transaction Details</h3>
          <div class="mt-2 px-7 py-3">
            <pre class="text-left whitespace-pre-wrap break-words">{{ prettyJson }}</pre>
          </div>
          <div class="items-center px-4 py-3">
            <button
              @click="closeModal"
              class="px-4 py-2 bg-blue-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-300"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import { Oracle, useGenlayerStore } from '../stores/genlayerStore';

import Address from './Address.vue';
import { onMounted, ref, computed } from 'vue';
import { Address as AddressType } from 'genlayer-js/types';

const route = useRoute();
const genlayerStore = useGenlayerStore();
const oracle = ref<Oracle>();

interface Transaction {
  consensus_data: {
    final: boolean;
    validators: {
      address: string;
      // Add other validator properties if needed
    }[];
    votes: {
      [key: string]: string;
    };
    leader_receipt: {
      args: string[][];
      class_name: string;
      contract_state: string;
      eq_outputs: {
        leader: {
          [key: string]: string;
        };
      };
      error: string | null;
      execution_result: string;
      gas_used: number;
      method: string;
      mode: string;
      node_config: {
        address: string;
        config: Record<string, unknown>;
        model: string;
        plugin: string;
        plugin_config: {
          api_key_env_var: string;
          api_url: string | null;
        };
        provider: string;
        stake: number;
      };
      vote: string;
    };
  };
  created_at: string;
  data: {
    function_args: string;
    function_name: string;
  };
  from_address: string;
  gaslimit: number;
  hash: string;
  leader_only: boolean;
  nonce: number;
  r: string | null;
  s: string | null;
  status: string;
  to_address: string;
  triggered_by: string | null;
  triggered_transactions: any[];
  type: number;
  v: string | null;
  value: number;
}

const transactions = ref<Transaction[]>([]);
const showModal = ref(false);
const selectedTransaction = ref<Transaction | null>(null);

onMounted(async () => {
  await loadOracle();
  console.log(transactions.value)
});

async function loadOracle() {
  oracle.value = (await genlayerStore.oracles).find(oracle => oracle.address === route.params.address);
  transactions.value = await genlayerStore.client.request( // TODO: fix typing and explore alternatives to sim_getTransactionsForAddress, since it's not a GenLayer method (could be problematic when going to mainnet)
    {
      method: "sim_getTransactionsForAddress",
      params: [route.params.address]
    }
  )
}

// Add refresh function
async function refreshOracle() {
  await genlayerStore.fetchOracle(route.params.address as AddressType);
  await loadOracle();
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'Not specified';
  const date = new Date(dateString);
  return date.toLocaleString();
};

function openModal(tx: Transaction) {
  selectedTransaction.value = tx;
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  selectedTransaction.value = null;
}

const prettyJson = computed(() => {
  if (!selectedTransaction.value) return '';
  return JSON.stringify(selectedTransaction.value, null, 2);
});
</script>

<style scoped>
pre {
  max-height: 60vh;
  overflow-y: auto;
}
</style>
