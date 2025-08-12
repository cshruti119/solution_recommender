import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3001,
    strictPort: true,
    proxy: {
      '/recommend': {
        target: 'http://localhost:8083',
        changeOrigin: true,
        secure: false
      }
    }
  }
});
