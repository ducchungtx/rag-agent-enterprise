import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

const apiProxy = {
  target: "http://127.0.0.1:8000",
  changeOrigin: true,
};

export default defineConfig({
  plugins: [react(), tailwindcss()],
  base: "/ui/",
  server: {
    port: 5173,
    proxy: {
      "/auth": apiProxy,
      "/tenants": apiProxy,
      "/kb": apiProxy,
      "/documents": apiProxy,
      "/chat": apiProxy,
      "/agent": apiProxy,
      "/search": apiProxy,
      "/api-keys": apiProxy,
      "/audit": apiProxy,
      "/health": apiProxy,
      "/mcp": apiProxy,
    },
  },
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
});
