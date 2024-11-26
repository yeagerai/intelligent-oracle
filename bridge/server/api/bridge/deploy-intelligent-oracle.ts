import { defineEventHandler, readBody } from "h3";
import { createAccount, createClient } from "genlayer-js";
import { simulator } from "genlayer-js/chains";
import { Address, TransactionStatus } from "genlayer-js/types";
import { intelligentOracleCode } from "../../../contracts/intelligent-oracle";

// Set max duration to 30 seconds in Vercel deployment
export const maxDuration = 30;

interface IntelligentOracleInput {
  predictionMarketId: string;
  title: string;
  description: string;
  potentialOutcomes: string[];
  rules: string[];
  dataSourceDomains: string[];
  resolutionURLs: string[];
  earliestResolutionDate: string;
}

const { bridgePrivateKey, simulatorUrl, icRegistryAddress } = useRuntimeConfig();

function validateInput(input: IntelligentOracleInput): string | null {
  const requiredFields: (keyof IntelligentOracleInput)[] = [
    "title",
    "description",
    "potentialOutcomes",
    "rules",
    "earliestResolutionDate",
  ];

  for (const field of requiredFields) {
    if (!input[field] || (Array.isArray(input[field]) && input[field].length === 0)) {
      return `Missing or empty field: ${field}`;
    }
  }

  if (
    (!input.resolutionURLs && !input.dataSourceDomains) ||
    (Array.isArray(input.resolutionURLs) &&
      Array.isArray(input.dataSourceDomains) &&
      input.resolutionURLs.length === 0 &&
      input.dataSourceDomains.length === 0)
  ) {
    return "Missing resolution URLs or data source domains.";
  }

  return null;
}

export default defineEventHandler(async (event) => {
  try {
    // Add CORS headers
    setResponseHeaders(event, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "*",
      "Access-Control-Allow-Headers": "Content-Type",
    });
    // Handle OPTIONS request for CORS preflight
    if (event.method === "OPTIONS") {
      return "OK";
    }
    const body = await readBody(event);
    const validationError = validateInput(body);

    if (validationError) {
      return {
        status: "error",
        message: validationError,
      };
    }

    const account = createAccount(bridgePrivateKey as `0x${string}`);
    const client = createClient({
      chain: simulator,
      account: account, // Optional: Use this account for subsequent calls
      endpoint: simulatorUrl,
    });
    console.log("🚀 ~ simulatorUrl:", simulatorUrl);

    const deploymentArgs = [
      body.predictionMarketId || "0",
      body.title,
      body.description,
      body.potentialOutcomes,
      body.rules,
      body.dataSourceDomains || [],
      body.resolutionURLs || [],
      body.earliestResolutionDate,
    ];
    console.log("🚀 ~ Deploy Intelligent Contract ~ deploymentArgs:", deploymentArgs);
    const transactionHash = await client.deployContract({
      code: intelligentOracleCode,
      args: deploymentArgs,
    });
    console.log("🚀 ~ Deploy Intelligent Contract ~ transactionHash:", transactionHash);

    const receipt = await client.waitForTransactionReceipt({
      hash: transactionHash,
      status: TransactionStatus.FINALIZED, // or 'ACCEPTED'
    });
    console.log("🚀 ~ Deploy Intelligent Contract ~ receipt:", receipt);

    // @ts-ignore
    if (
      !receipt.consensus_data?.leader_receipt?.execution_result ||
      receipt.consensus_data?.leader_receipt?.execution_result !== "SUCCESS"
    ) {
      return {
        status: "error",
        message: "Intelligent Oracle deployment failed",
      };
    }

    const contractAddress = receipt.data?.contract_address as `0x${string}`;
    console.log("🚀 ~ Deploy Intelligent Contract ~ registering contract: ", contractAddress);

    const registerContractTransactionHash = await client.writeContract({
      address: icRegistryAddress as Address,
      functionName: "register_contract",
      args: [contractAddress],
      value: BigInt(0),
    });

    await client.waitForTransactionReceipt({
      hash: registerContractTransactionHash,
      status: TransactionStatus.FINALIZED,
    });

    return {
      status: "success",
      message: "Intelligent Oracle deployed successfully",
      receipt,
    };
  } catch (error) {
    console.error("Error deploying Intelligent Oracle:", error);
    return {
      status: "error",
      message: "An error occurred while deploying the Intelligent Oracle",
    };
  }
});
