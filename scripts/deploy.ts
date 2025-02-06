import { config } from "dotenv";
import { readFileSync } from "fs";
import { createAccount, createClient } from "genlayer-js";
import { simulator } from "genlayer-js/chains";
import { TransactionHash, TransactionStatus } from "genlayer-js/types";
import JSZip from "jszip";
import path from "path";

// Configure dotenv at the top of the file
config();

const account = createAccount();
const client = createClient({
  chain: simulator,
  endpoint: process.env.RPC_URL || undefined,
  account: account,
});

function checkReceiptSuccess(receipt: any, context: string = "Transaction"): void {
  if (receipt.consensus_data?.leader_receipt?.execution_result !== "SUCCESS") {
    throw new Error(`${context} failed. Receipt: ${JSON.stringify(receipt)}`);
  }
}

async function zipContract(files: { path: string; content: string }[]): Promise<Buffer> {
  // Create a new JSZip instance
  const zip = new JSZip();

  // Add files to the zip
  for (const { path, content } of files) {
    zip.file(path, content);
  }

  // Generate zip buffer
  const buffer = await zip.generateAsync({ type: "nodebuffer" });

  // Deploy the contract
  return buffer;
}

async function getIntelligentOracleFactoryCode(): Promise<Uint8Array> {
  const zippedCode = await zipContract([
    {
      path: "src/__init__.py",
      content: readFileSync(
        path.join(__dirname, "../intelligent-contracts/IntelligentOracleFactory.py"),
        "utf8"
      ),
    },
    {
      path: "src/IntelligentOracle.py",
      content: readFileSync(path.join(__dirname, "../intelligent-contracts/IntelligentOracle.py"), "utf8"),
    },
    {
      path: "runner.json",
      content: readFileSync(path.join(__dirname, "../intelligent-contracts/runner.json"), "utf8"),
    },
  ]);
  return new Uint8Array(zippedCode);
}

const main = async () => {
  await client.initializeConsensusSmartContract();
  const contractsCode = await getIntelligentOracleFactoryCode();

  const deployTransaction = await client.deployContract({
    code: contractsCode,
    args: [],
  });
  console.log("Deploy Transaction:", deployTransaction);

  const receipt = await client.waitForTransactionReceipt({
    hash: deployTransaction as TransactionHash,
    status: TransactionStatus.ACCEPTED,
    retries: 200,
  });

  console.log("Transaction receipt:", receipt);

  checkReceiptSuccess(receipt, "Contract deployment");

  const address = receipt.data?.contract_address as string;
  console.log(`Deployed contract to address: ${address}`);
};

main().catch(console.error);
