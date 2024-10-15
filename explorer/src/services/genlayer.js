import { createClient, createAccount as createGenLayerAccount, generatePrivateKey } from "genlayer-js";
import { simulator } from "genlayer-js/chains";

const accountPrivateKey = localStorage.getItem("accountPrivateKey")
  ? localStorage.getItem("accountPrivateKey")
  : null;
export const account = accountPrivateKey ? createGenLayerAccount(accountPrivateKey) : null;

export const createAccount = () => {
  const newAccountPrivateKey = generatePrivateKey();
  localStorage.setItem("accountPrivateKey", newAccountPrivateKey);
  return createGenLayerAccount(newAccountPrivateKey);
};

export const client = createClient({ chain: simulator, account, endpoint: import.meta.env.VITE_SIMULATOR_RPC_URL });
