<script setup lang="ts">
import { useRuntimeConfig } from "#app";
import { useChat } from "@ai-sdk/vue";
import { computed, ref, onMounted, nextTick, watch } from "vue";
import confetti from "canvas-confetti";
import Prism from "prismjs";
import "prismjs/themes/prism-tomorrow.css";
import "prismjs/components/prism-json";

// Function to highlight JSON
const highlightJson = (code: string) => {
  return Prism.highlight(code, Prism.languages.json, "json");
};

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

// Add a ref for the messages container
const messagesContainer = ref<HTMLDivElement | null>(null);

// Add a function to scroll to bottom
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

const { error, input, isLoading, messages, handleSubmit, reload, stop, append } = useChat({
  api: config.public.chatApiUrl as string,
  keepLastMessageOnError: true,
  onFinish(message, { usage, finishReason }) {
    console.log("Usage", usage);
    console.log("FinishReason", finishReason);
    setTimeout(() => {
      inputRef.value?.focus();
      scrollToBottom();
    }, 0);
  },
});

// Add watch to handle scrolling when messages change
watch(messages, () => {
  nextTick(() => {
    scrollToBottom();
  });
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
  const jsonRegex = /```json\n([\s\S]*?)(?:```|$)/g;
  const match = jsonRegex.exec(content);

  if (!match) {
    return {
      formattedContent: {
        beforeJson: content,
        afterJson: "",
      },
    };
  }

  try {
    // Split content into parts before and after the JSON block
    const [beforeJson, ...afterJsonParts] = content.split(jsonRegex);
    console.log("🚀 ~ formatMessage ~ beforeJson:", beforeJson);
    const afterJson = afterJsonParts.slice(1).join("").trim();
    console.log("🚀 ~ formatMessage ~ afterJson:", afterJson);

    // Format the content with the JSON removed
    const formattedContent = {
      beforeJson: beforeJson.trim(),
      afterJson: afterJson ? `\n${afterJson}` : "",
    };

    const parsedJson = JSON.parse(match[1]);
    const formattedJson = JSON.stringify(parsedJson, null, 2);
    const highlightedJson = highlightJson(formattedJson);

    return {
      formattedContent,
      jsonContent: parsedJson,
      highlightedJson,
    };
  } catch (e) {
    const formattedContent = {
      beforeJson: content.replace(
        jsonRegex,
        `<pre><code class="language-json">Generating JSON...</code></pre>`
      ),
      afterJson: "",
    };
    return {
      formattedContent,
    };
  }
};

const lastJsonMessageId = computed(() => {
  for (let i = messages.value.length - 1; i >= 0; i--) {
    if (formatMessage(messages.value[i].content).jsonContent) {
      return messages.value[i].id;
    }
  }
  return null;
});
</script>

<template>
  <div class="min-h-screen bg-background">
    <div
      ref="messagesContainer"
      class="flex flex-col w-full max-w-3xl h-[calc(100vh-8rem)] mx-auto stretch text-primary-text font-sans overflow-y-auto px-4"
    >
      <div class="py-24">
        <div v-for="m in messages.slice(1)" :key="m.id" class="whitespace-pre-wrap mb-4">
          <span class="font-bold" :class="{ 'text-highlight': m.role !== 'user' }">{{
            m.role === "user" ? "You: " : "Intelligent Oracle Assistant: "
          }}</span>
          <span v-html="formatMessage(m.content).formattedContent.beforeJson"></span>
          <div v-if="formatMessage(m.content).jsonContent" class="json-viewer-wrapper">
            <pre><code class="language-json" v-html="formatMessage(m.content).highlightedJson"></code></pre>
          </div>
          <span v-html="formatMessage(m.content).formattedContent.afterJson"></span>
          <div v-if="m.id === lastJsonMessageId" class="flex flex-col gap-2">
            <div class="flex gap-2">
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
            </div>

            <div
              v-if="deployedOracleAddress"
              class="mt-4 p-6 bg-green-100 rounded-lg border border-green-800"
            >
              <p class="text-green-800 text-lg mb-4">
                Your Intelligent Oracle has been successfully deployed at:
                <span class="font-mono font-medium block mt-2">{{ deployedOracleAddress }}</span>
              </p>
              <a
                :href="`${config.public.explorerUrl}/oracle/${deployedOracleAddress}`"
                target="_blank"
                class="inline-flex items-center px-4 py-2 bg-green-700 text-white rounded-md transition-colors"
              >
                View in the explorer
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-4 w-4 ml-2"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                  />
                </svg>
              </a>
            </div>
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

.dark .bg-green-100 {
  background-color: rgba(6, 78, 59, 0.2);
}

@media (prefers-color-scheme: dark) {
  .bg-green-100 {
    background-color: rgba(6, 78, 59, 0.2);
  }
}

.json-viewer-wrapper {
  margin: 1em 0;
}

.json-viewer-wrapper pre {
  margin: 0;
  background-color: #1e1e1e;
  border-radius: 6px;
  padding: 1rem;
  overflow-x: auto;
}

.json-viewer-wrapper code {
  font-family: "Fira Code", monospace;
  font-size: 0.9em;
}

/* Light mode overrides */
@media (prefers-color-scheme: light) {
  .json-viewer-wrapper pre {
    background-color: #f5f5f5;
  }
}

/* Hide scrollbar but maintain scroll functionality */
.overflow-y-auto {
  scroll-behavior: smooth;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* Internet Explorer/Edge */
}

/* WebKit browsers (Chrome, Safari) */
.overflow-y-auto::-webkit-scrollbar {
  display: none;
}
</style>
