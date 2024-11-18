# GenLayer Intelligent Oracle Configuration Wizard

## Overview

This project implements a chatbot wizard to assist developers in configuring intelligent oracles for the GenLayer blockchain protocol. The wizard guides users through the process of setting up AI-powered prediction markets using GenLayer's Intelligent Contracts platform.

## Features

- Interactive chatbot interface
- Step-by-step configuration of Intelligent Oracles
- Integration with OpenAI's GPT-4 for natural language processing
- Real-time streaming of AI responses
- Tailwind CSS for modern, responsive design

## Technologies Used

- Vue.js 3
- Nuxt.js 3
- Tailwind CSS
- OpenAI GPT-4
- Vercel Edge Functions

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   npm install
   ```
3. Set up environment variables:
   Create a `.env` file in the root directory and add:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Configuration

The project uses Nuxt.js configuration. Key settings can be found in `nuxt.config.ts`.

Tailwind CSS is configured in `tailwind.config.js`.

## Usage

1. Start the development server:
   ```
   npm run dev
   ```
2. Open your browser and navigate to `http://localhost:3000`
3. Follow the chatbot's prompts to configure your Intelligent Oracle

## API

The backend of this project is implemented in the [bridge](../bridge) section of this repository. It includes the chat API and the endpoints to interact with the GenLayer blockchain to deploy and register every prediction market.


## Customization

To modify the initial prompt or change the behavior of the chatbot, edit the [`initialPrompt` constant in `bridge/server/api/chat.ts`](../bridge/server/api/chat.ts).
