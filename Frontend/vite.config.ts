<<<<<<< HEAD
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
    port: 5173        
  }
});
=======
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),  
  ],
});
>>>>>>> feature/trip-graph-api
