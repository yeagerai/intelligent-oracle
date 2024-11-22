import { defineStore } from "pinia";
import { createClient, createAccount as createGenLayerAccount, generatePrivateKey } from "genlayer-js";
import { simulator } from "genlayer-js/chains";
import { ref, computed } from "vue";
import { Address } from "genlayer-js/types";

export interface Oracle {
  title: string;
  address: Address;
  potential_outcomes: string[];
  rules: string[];
  status: string;
  outcome: string | null;
  creator: string;
  earliest_resolution_date: string;
  description: string;
  prediction_market_id: string;
  valid_data_sources: string[];
  data_source_domains: string[];
  resolution_urls: string[];
  analysis: string;
}

// This store is for:
// - storing the private key for the account in local storage
// - providing one account and client to the whole app
// - caching the oracles
// It might be a good idea to split it into multiple stores, dependant on each other
export const useGenlayerStore = defineStore("genlayer", () => {
  const client = computed(() =>
    createClient({
      chain: simulator,
      account: account.value,
      endpoint: import.meta.env.VITE_SIMULATOR_RPC_URL,
    })
  );

  // Account
  const accountPrivateKey = ref(localStorage.getItem("accountPrivateKey") || null);

  const account = computed(() => {
    if (!accountPrivateKey.value) {
      createAccount();
    }
    return createGenLayerAccount(accountPrivateKey.value as Address);
  });

  function createAccount() {
    const newAccountPrivateKey = generatePrivateKey();
    accountPrivateKey.value = newAccountPrivateKey;
    localStorage.setItem("accountPrivateKey", newAccountPrivateKey);
  }

  // Oracles

  const _oracles = ref<Oracle[]>([]);
  const oracles = computed(async () => {
    if (_oracles.value.length === 0) {
      await refreshOracles();
    }
    return _oracles.value;
  });

  async function refreshOracles() {
    const registryContractAddress = import.meta.env.VITE_CONTRACT_ADDRESS as Address;
    console.log("registryContractAddress", registryContractAddress);
    const contract_addresses: Address[] = await client.value.readContract({
      account: account.value,
      address: registryContractAddress,
      functionName: "get_contract_addresses",
      args: [],
    });

    _oracles.value = await Promise.all(contract_addresses.map((address) => fetchOracle(address)));
  }

  async function fetchOracle(address: Address): Promise<Oracle> {
    console.log("fetchOracle", address);
    return await client.value
      .readContract({
        account: account.value,
        address,
        functionName: "get_dict",
        args: [],
      })
      .then((result) => ({ ...result, address }))
      .catch((error) => {
        console.error("Error fetching oracle:", error);
        return { address, error: "Error fetching oracle" };
      });
  }

  async function resolveOracle(address: Address, evidence: string): Promise<Oracle> {
    console.log("resolveOracle", address);
    return await client.value
      .writeContract({
        account: account.value,
        address,
        functionName: "resolve",
        args: evidence ? [evidence] : [],
        value: BigInt(0),
      })
      .then((result) => ({ ...result, address }));
  }

  return {
    accountPrivateKey,
    client,
    account,
    oracles,
    refreshOracles,
    fetchOracle,
    resolveOracle,
  };
});
