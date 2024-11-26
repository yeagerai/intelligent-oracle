import { defineNitroConfig } from "nitropack";

// Set max duration to 30 seconds in Vercel deployment
export default defineNitroConfig({
  vercel: {
    functions: {
      maxDuration: 15,
    },
  },
});
