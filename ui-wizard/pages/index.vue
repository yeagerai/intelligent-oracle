<script setup lang="ts">
import { useRuntimeConfig } from "#app";
import { useChat } from "@ai-sdk/vue";
import { computed, ref, onMounted } from "vue";
import confetti from "canvas-confetti";

enum DEPLOYMENT_STATUS {
  NONE = "NONE",
  DEPLOYING = "DEPLOYING",
  DEPLOYED = "DEPLOYED",
  FAILED = "FAILED",
}

const getDeployButtonTextFromStatus = (status: DEPLOYMENT_STATUS) => {
  if (status === DEPLOYMENT_STATUS.DEPLOYING) {
    return "Deploying...";
  }
  if (status === DEPLOYMENT_STATUS.DEPLOYED) {
    return "Deployed";
  }
  if (status === DEPLOYMENT_STATUS.FAILED) {
    return "Deployment Failed";
  }
  return "Deploy";
};

const config = useRuntimeConfig();
const chatInitiated = ref(false);
const configCopied = ref(false);
const deployedOracleAddress = ref("");
const icDeploymentStatus = ref(DEPLOYMENT_STATUS.NONE);
const inputRef = ref<HTMLInputElement | null>(null);

const { error, input, isLoading, messages, handleSubmit, reload, stop, append } = useChat({
  api: config.public.chatApiUrl as string,
  keepLastMessageOnError: true,
  onFinish(message, { usage, finishReason }) {
    console.log("Usage", usage);
    console.log("FinishReason", finishReason);
    setTimeout(() => {
      inputRef.value?.focus();
    }, 0);
  },
});

const sendMessage = (e: Event) => {
  e.preventDefault();
  icDeploymentStatus.value = DEPLOYMENT_STATUS.NONE;
  handleSubmit();
};

const disabled = computed(() => isLoading.value || error.value != null);

const startChat = () => {
  append({
    role: "user",
    content: "__start__",
  });
  chatInitiated.value = true;
  setTimeout(() => {
    inputRef.value?.focus();
  }, 0);
};

onMounted(() => {
  setTimeout(() => {
    startChat();
  }, 1000);
});

const copyToClipboard = (text: string) => {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      configCopied.value = true;
      setTimeout(() => {
        configCopied.value = false;
      }, 1500);
    })
    .catch((err) => {
      console.error("Failed to copy text: ", err);
    });
};

const deployIntelligentContract = async (jsonContent: string) => {
  try {
    icDeploymentStatus.value = DEPLOYMENT_STATUS.DEPLOYING;
    const response = await fetch(`${config.public.bridgeApiUrl}/deploy-intelligent-oracle`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: jsonContent,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();

    if (result.status === "error") {
      throw new Error(`Deployment failed: ${result.message}`);
    }

    deployedOracleAddress.value = result.receipt.data.contract_address;
    console.log("Deployment successful:", result);

    // Trigger confetti animation
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
    });

    // Update button text and disable it
    icDeploymentStatus.value = DEPLOYMENT_STATUS.DEPLOYED;
  } catch (error) {
    console.error("Error deploying Intelligent Contract:", error);
    icDeploymentStatus.value = DEPLOYMENT_STATUS.FAILED;
  } finally {
  }
};

const formatMessage = (content: string) => {
  const jsonRegex = /```json\n([\s\S]*?)```/g;
  const match = jsonRegex.exec(content);

  if (!match) {
    return {
      formattedContent: content,
      jsonContent: null,
    };
  }

  try {
    const parsedJson = JSON.parse(match[1]);
    const formattedContent = content.replace(
      jsonRegex,
      `<pre><code class="language-json">${JSON.stringify(parsedJson, null, 2)}</code></pre>`
    );

    return {
      formattedContent,
      jsonContent: parsedJson,
    };
  } catch (e) {
    return {
      formattedContent: content,
      jsonContent: null,
    };
  }
};
</script>

<template>
  <div class="min-h-screen bg-background">
    <div class="flex flex-col w-full max-w-2xl py-24 mx-auto stretch text-primary-text font-sans">
      <div v-for="m in messages.slice(1)" :key="m.id" class="whitespace-pre-wrap mb-4">
        <span class="font-bold" :class="{ 'text-highlight': m.role !== 'user' }">{{
          m.role === "user" ? "You: " : "Intelligent Oracle Assistant: "
        }}</span>
        <span v-html="formatMessage(m.content).formattedContent"> </span>
        <div v-if="formatMessage(m.content).jsonContent" class="flex gap-2">
          <button
            @click="copyToClipboard(JSON.stringify(formatMessage(m.content).jsonContent, null, 2))"
            class="msg-btn copy-btn"
          >
            {{ configCopied ? "Copied!" : "Copy to Clipboard" }}
          </button>
          <button
            @click="deployIntelligentContract(JSON.stringify(formatMessage(m.content).jsonContent))"
            :disabled="
              icDeploymentStatus === DEPLOYMENT_STATUS.DEPLOYING ||
              icDeploymentStatus === DEPLOYMENT_STATUS.DEPLOYED
            "
            class="msg-btn deploy-btn bg-highlight text-white border border-highlight"
          >
            {{ getDeployButtonTextFromStatus(icDeploymentStatus) }}
          </button>
          <a
            v-if="deployedOracleAddress"
            :href="`${config.public.explorerUrl}/oracle/${deployedOracleAddress}`"
            target="_blank"
            class="msg-btn px-4 py-1"
            >View in the explorer: {{ deployedOracleAddress }}</a
          >
        </div>
      </div>

      <div v-if="isLoading" class="mt-4 text-secondary-text">
        <div>Loading...</div>
        <button
          type="button"
          class="px-4 py-2 mt-4 text-highlight border border-highlight rounded-xl hover:bg-highlight hover:text-primary-text transition-colors"
          @click="stop"
        >
          Stop
        </button>
      </div>

      <div v-if="error" class="mt-4">
        <div class="text-accent">An error occurred.</div>
        <button
          type="button"
          class="px-4 py-2 mt-4 text-highlight border border-highlight rounded-xl hover:bg-highlight hover:text-primary-text transition-colors"
          @click="() => reload()"
        >
          Retry
        </button>
      </div>

      <div class="mt-8">
        <form @submit="sendMessage" class="fixed bottom-0 flex gap-2 w-full max-w-md mb-8">
          <input
            ref="inputRef"
            class="flex-1 p-4 border border-highlight rounded-xl shadow-xl bg-background text-primary-text placeholder-secondary-text"
            v-model="input"
            placeholder="Say something..."
            :disabled="disabled"
          />
          <button
            type="submit"
            :disabled="disabled"
            class="px-4 py-2 bg-highlight text-white rounded-xl hover:bg-opacity-90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style>
pre {
  background-color: #2a2a2a;
  padding: 1em;
  border-radius: 4px;
  overflow-x: auto;
  color: #e0e0e0;
  border: 1px solid #444;
}

code {
  font-family: "Courier New", Courier, monospace;
  color: #e0e0e0;
}

@media (prefers-color-scheme: light) {
  pre {
    background-color: #f0f0f0;
    color: #333;
    border: 1px solid #ccc;
  }

  code {
    color: #333;
  }
}

.msg-btn {
  display: block;
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.copy-btn {
  background-color: #4a4a4a;
  color: #fff;
}
.copy-btn:hover {
  background-color: #5a5a5a;
}

@media (prefers-color-scheme: light) {
  .copy-btn {
    background-color: #e0e0e0;
    color: #333;
  }

  .copy-btn:hover {
    background-color: #d0d0d0;
  }
}

.deploy-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #808080;
  border-color: #808080;
}

@media (prefers-color-scheme: light) {
  .deploy-btn:disabled {
    background-color: #d0d0d0;
    border-color: #d0d0d0;
    color: #666;
  }
}
</style>
