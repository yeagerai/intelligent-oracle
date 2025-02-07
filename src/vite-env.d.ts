interface ImportMetaEnv {
  VITE_SIMULATOR_RPC_URL: string;
  VITE_CONTRACT_ADDRESS: string;
  VITE_CHAT_URL: string;
  // Add other environment variables as needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
