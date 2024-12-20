<template>
  <div class="min-h-screen bg-background text-primary-text">
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
        <div class="flex items-center space-x-4">
          <router-link 
            to="/" 
            class="text-4xl font-medium py-2 cursor-pointer"
          >
          &#9204;
          </router-link>
          <h1 class="text-3xl font-bold text-primary-text">Oracle Details</h1>
        </div>
        <div class="flex space-x-4">
          <button @click="refreshOracle" class="px-4 py-2 border border-highlight text-highlight bg-white rounded hover:bg-highlight/10 transition-colors">
            Refresh Data
          </button>
          <button @click="openResolutionModal" class="px-4 py-2 bg-highlight text-white rounded hover:opacity-80 transition-colors">
            Initiate Resolution
          </button>
        </div>
      </div>
    </header>
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div v-if="oracle" class="flex space-x-6">
        <div class="bg-white shadow overflow-hidden sm:rounded-lg flex-1">
          <div class="px-4 py-5 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-primary-text">{{ oracle.title }}</h3>
            <p class="mt-1 max-w-2xl text-sm text-secondary-text">
              <Address :address="oracle.address" :showFull="true" />
            </p>
          </div>
          <div class="border-t border-gray-200 px-4 py-5 sm:p-0">
            <dl class="sm:divide-y sm:divide-gray-200">
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-secondary-text">Status</dt>
                <dd class="mt-1 text-sm text-primary-text sm:mt-0 sm:col-span-2">
                  <span :class="{
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium': true,
                    'bg-highlight/20 text-highlight': oracle.status === 'Active',
                    'bg-green-100 text-green-800': oracle.status === 'Resolved',
                    'bg-red-100 text-red-800': oracle.status === 'Error'
                  }">
                    {{ oracle.status }}
                  </span>
                </dd>
              </div>
              <div v-if="oracle.outcome" class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-secondary-text">Outcome</dt>
                <dd class="mt-1 text-sm text-primary-text sm:mt-0 sm:col-span-2">{{ oracle.outcome || 'Not yet determined' }}</dd>
              </div>
              
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-secondary-text">Description</dt>
                <dd class="mt-1 text-sm text-primary-text sm:mt-0 sm:col-span-2">{{ oracle.description }}</dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-secondary-text">Potential Outcomes</dt>
                <dd class="mt-1 text-sm text-primary-text sm:mt-0 sm:col-span-2">
                  <ul class="list-disc pl-5">
                    <li v-for="outcome in oracle.potential_outcomes" :key="outcome">{{ outcome }}</li>
                  </ul>
                </dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-secondary-text">Rules</dt>
                <dd class="mt-1 text-sm text-primary-text sm:mt-0 sm:col-span-2">
                  <ul class="list-disc pl-5">
                    <li v-for="rule in oracle.rules" :key="rule">{{ rule }}</li>
                  </ul>
                </dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-secondary-text">Data Source Domains:</dt>
                <dd class="mt-1 text-sm text-primary-text sm:mt-0 sm:col-span-2">
                  <ul v-if="oracle.data_source_domains.length > 0" class="list-disc pl-5">
                    <li v-for="domain in oracle.data_source_domains" :key="domain">{{ domain }}</li>
                  </ul>
                  <div v-else>This oracle uses fixed resolution URLs</div>
                </dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-secondary-text">Resolution URLs:</dt>
                <dd class="mt-1 text-sm text-primary-text sm:mt-0 sm:col-span-2">
                  <ul v-if="oracle.resolution_urls && oracle.resolution_urls.length > 0" class="list-disc pl-5">
                    <li v-for="url in oracle.resolution_urls" :key="url">{{ url }}</li>
                  </ul>
                  <div v-else>This oracle uses dynamic evidence URLs</div>
                </dd>
              </div>

              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-secondary-text">Earliest Resolution Date</dt>
                <dd class="mt-1 text-sm text-primary-text sm:mt-0 sm:col-span-2">{{ formatDate(oracle.earliest_resolution_date) }}</dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-secondary-text">Prediction Market ID</dt>
                <dd class="mt-1 text-sm text-primary-text sm:mt-0 sm:col-span-2">{{ oracle.prediction_market_id }}</dd>
              </div>
              <div class="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                <dt class="text-sm font-medium text-secondary-text">Analysis</dt>
                <dd class="mt-1 text-sm text-primary-text sm:mt-0 sm:col-span-2">
                  <div v-if="oracle.analysis" class="whitespace-pre-wrap break-words">
                    <div v-if="oracle.analysis.justification || oracle.analysis.reasoning">{{ oracle.analysis.justification || oracle.analysis.reasoning }}</div>
                    <div v-else>No analysis available</div>
                  </div>
                  <div v-else>No analysis available</div>
                </dd>
              </div>
            </dl>
          </div>
        </div>
        <div class="bg-white shadow overflow-hidden sm:rounded-lg flex-1">
          <div class="px-4 py-5 sm:px-6">
            <h3 class="text-lg leading-6 font-medium text-primary-text">Transactions</h3>
          </div>
          <div class="border-t border-gray-200">
            <ul class="divide-y divide-gray-200">
              <li v-for="tx in transactions" :key="tx.hash" class="px-4 py-4 cursor-pointer hover:bg-gray-50" @click="openTransactionModal(tx)">
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium text-highlight truncate">
                    {{ tx.hash }}
                  </p>
                  <div class="ml-2 flex-shrink-0 flex">
                    <p class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="tx.status === 'PENDING' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'">
                      {{ tx.status }}
                    </p>
                  </div>
                </div>
                <div class="mt-2">
                  <p class="text-sm text-secondary-text">Created at: {{ formatDate(tx.created_at) }}</p>
                  <p class="text-sm text-secondary-text">Nonce: {{ tx.nonce }}</p>
                  <div v-if="tx.status !== 'PENDING'">
                    <h4 class="text-sm font-medium text-primary-text mt-2">Validators and Votes:</h4>
                    <template v-if="tx.consensus_data && Object.entries(tx.consensus_data.votes).length > 0">
                      <ul class="mt-1 space-y-1">
                        <li v-for="validator in Object.entries(tx.consensus_data.votes)" :key="validator[0]" class="text-sm text-secondary-text">
                          {{ validator[0] }}: {{ tx.consensus_data.votes[validator[0]] || 'No vote' }}
                        </li>
                      </ul>
                    </template>
                    <template v-else>
                      <p class="mt-1 text-sm text-secondary-text">Leader only execution</p>
                    </template>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-8">
        <p class="text-xl text-secondary-text">Loading oracle details...</p>
      </div>
    </main>

    <!-- Transaction DetailsModal -->
    <div v-if="showTransactionModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" @click="closeTransactionModal">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white" @click.stop>
        <div class="mt-3 text-center">
          <h3 class="text-lg leading-6 font-medium text-primary-text">Transaction Details</h3>
          <div class="mt-2 px-7 py-3">
            <pre class="text-left whitespace-pre-wrap break-words">{{ prettyJson }}</pre>
          </div>
          <div class="items-center px-4 py-3 space-y-2">
            <button
              @click="copyToClipboard"
              class="px-4 py-2 bg-green-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-300"
            >
              Copy to Clipboard
            </button>
            <button
              @click="closeTransactionModal"
              class="px-4 py-2 bg-highlight text-white text-base font-medium rounded-md w-full shadow-sm hover:opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Resolution Modal -->
    <div v-if="showResolutionModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" @click="closeModal">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white" @click.stop>
        <div class="mt-3 text-center">
          <h3 class="text-lg leading-6 font-medium text-primary-text">Provide a URL for resolution</h3>
          <div class="mt-2 px-7 py-3">
            <input v-model="resolutionEvidence" type="text" class="w-full h-12 border border-gray-300 rounded-md p-2" placeholder="Enter evidence URL">
          </div>
          <div class="items-center px-4 py-3 space-y-2">
            <button
              @click="resolveOracle"
              class="px-4 py-2 bg-green-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-300"
            >
              Submit Resolution
            </button>
            <button
              @click="closeResolutionModal"
              class="px-4 py-2 bg-highlight text-white text-base font-medium rounded-md w-full shadow-sm hover:opacity-80 focus:outline-none focus:ring-2 focus:ring-highlight"
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
import { onMounted, ref, computed, onUnmounted } from 'vue';
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
const showTransactionModal = ref(false);
const selectedTransaction = ref<Transaction | null>(null);
const showResolutionModal = ref(false);
const resolutionEvidence = ref<string>("");
const refreshInterval = ref<number>();

onMounted(async () => {
  loadOracle();
  await refreshOracle();
  refreshInterval.value = window.setInterval(async () => {
    await refreshOracle();
  }, 5000);
});

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value);
  }
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

async function resolveOracle() {
  await genlayerStore.resolveOracle(route.params.address as AddressType, resolutionEvidence.value);
  await refreshOracle();
  await closeResolutionModal();
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'Not specified';
  const date = new Date(dateString);
  return date.toLocaleString();
};

function openTransactionModal(tx: Transaction) {
  selectedTransaction.value = tx;
  showTransactionModal.value = true;
}

function closeTransactionModal() {
  showTransactionModal.value = false;
  selectedTransaction.value = null;
}

function openResolutionModal() {
  if (oracle.value?.resolution_urls && oracle.value.resolution_urls.length > 0) {
    resolveOracle();
  } else {
    resolutionEvidence.value = "";
    showResolutionModal.value = true;
  }
}

function closeResolutionModal() {
  showResolutionModal.value = false;
  resolutionEvidence.value = "";
}

const prettyJson = computed(() => {
  if (!selectedTransaction.value) return '';
  console.log('🚀 ~ prettyJson ~ selectedTransaction:', selectedTransaction);
  return JSON.stringify({
    ...selectedTransaction.value,
    consensus_data: {
      ...selectedTransaction.value.consensus_data,
      leader_receipt: selectedTransaction.value.consensus_data?.leader_receipt ? {
        ...selectedTransaction.value.consensus_data.leader_receipt,
        contract_state: `${selectedTransaction.value.consensus_data.leader_receipt.contract_state.slice(0,10)}...${selectedTransaction.value.consensus_data.leader_receipt.contract_state.slice(-10)}`,
      } : undefined,
      validators: selectedTransaction.value.consensus_data?.validators.map((validator: any) => ({
        ...validator,
        eq_outputs: undefined,
        contract_state: `${validator.contract_state.slice(0,10)}...${validator.contract_state.slice(-10)}`,
      })),
    },
  }, null, 2);
});
  

function copyToClipboard() {
  if (selectedTransaction.value) {
    navigator.clipboard.writeText(JSON.stringify(selectedTransaction.value, null, 2))
      .then(() => {
        alert('Transaction data copied to clipboard!');
      })
      .catch((err) => {
        console.error('Failed to copy text: ', err);
        alert('Failed to copy transaction data. Please try again.');
      });
  }
}
</script>

<style scoped>
pre {
  max-height: 60vh;
  overflow-y: auto;
}
</style>
