<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <div class="w-64 bg-gray-800 text-white p-4">
      <h1 class="text-2xl font-bold mb-4">Chat Interface</h1>
      <!-- Add any sidebar content here -->
    </div>

    <!-- Main chat area -->
    <div class="flex-1 flex flex-col">
      <!-- Chat messages -->
      <div class="flex-1 overflow-y-auto p-4 space-y-4">
        <div v-for="(message, index) in messages" :key="index" class="flex">
          <div
            :class="[
              'max-w-3/4 p-3 rounded-lg',
              message.isUser ? 'bg-blue-500 text-white self-end' : 'bg-gray-200 text-gray-800 self-start'
            ]"
          >
            {{ message.content }}
          </div>
        </div>
      </div>

      <!-- Input area -->
      <div class="p-4 border-t border-gray-200">
        <form @submit.prevent="sendMessage" class="flex space-x-2">
          <input
            v-model="userInput"
            type="text"
            placeholder="Type your message..."
            class="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Sending...' : 'Send' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)

const sendMessage = async () => {
  if (userInput.value.trim() === '') return

  // Add user message
  messages.value.push({ content: userInput.value, isUser: true })

  // Clear input
  const userMessage = userInput.value
  userInput.value = ''

  // Set loading state
  isLoading.value = true

  try {
    // Fetch bot response from API
    const response = await fetch('https://api.example.com/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message: userMessage }),
    })

    if (!response.ok) {
      throw new Error('API request failed')
    }

    const data = await response.json()

    // Add bot message
    messages.value.push({ content: data.response, isUser: false })
  } catch (error) {
    console.error('Error fetching bot response:', error)
    messages.value.push({ content: 'Sorry, I encountered an error. Please try again.', isUser: false })
  } finally {
    isLoading.value = false
  }
}
</script>