import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './'),
      '@components': path.resolve(__dirname, './components'),
      '@hooks': path.resolve(__dirname, './hooks'),
      '@contexts': path.resolve(__dirname, './contexts'),
      '@services': path.resolve(__dirname, './services'),
      '@styles': path.resolve(__dirname, './styles'),
      '@assets': path.resolve(__dirname, './assets'),
    },
  },
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  build: {
    outDir: '../dashboard/static',
    emptyOutDir: true,
    sourcemap: true,
  },
});