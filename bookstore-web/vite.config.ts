import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const odooDb = env.VITE_ODOO_DB || 'odoo_dev'
  const odooTarget = env.VITE_ODOO_PROXY_TARGET || 'http://127.0.0.1:8069'

  return {
    plugins: [react()],
    server: {
      host: '127.0.0.1',
      port: 5173,
      proxy: {
        '/api': {
          target: odooTarget,
          changeOrigin: true,
          configure: (proxy) => {
            proxy.on('proxyReq', (proxyReq) => {
              proxyReq.setHeader('X-Odoo-Database', odooDb)
            })
          },
        },
      },
    },
  }
})
