import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  server: {
    host: "0.0.0.0",   // Allow access from other machines
    port: 7001
  }
});

// config.ts
// Use the actual server IP from .env, fallback to your server IP
export const API_BASE_URL = process.env.VITE_API_BASE_URL || "http://192.168.10.41:7001";
