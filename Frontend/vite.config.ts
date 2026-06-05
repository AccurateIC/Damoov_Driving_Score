import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),  
  ],
  server: {
    host: "0.0.0.0",  
    port: 7001        
  }
});

// config.ts
export const API_BASE_URL = process.env.REACT_APP_BASE_URL ;
