import { defineStore } from "pinia";
import {
  createClient,
  createAccount as createGenLayerAccount,
  generatePrivateKey,
} from "genlayer-js";
import { simulator } from "genlayer-js/chains";
import { ref, computed } from "vue";

export const useGenlayerStore = defineStore("genlayer", () => {
  const accountPrivateKey = ref(
    localStorage.getItem("accountPrivateKey") || null
  );
  const client = computed(() => {
    return createClient({
      chain: simulator,
      account: account.value as any,
      endpoint: import.meta.env.VITE_SIMULATOR_RPC_URL,
    });
  });

  const account = computed(() => {
    if (!accountPrivateKey.value) {
      createAccount();
    }
    return createGenLayerAccount(accountPrivateKey.value as any); // TODO: why is the Address type needed here?
  });

  function createAccount() {
    const newAccountPrivateKey = generatePrivateKey();
    accountPrivateKey.value = newAccountPrivateKey;
    localStorage.setItem("accountPrivateKey", newAccountPrivateKey);
  }

  return {
    accountPrivateKey,
    client,
    account,
  };
});
