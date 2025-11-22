import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  eslint: {
    // Deshabilitar ESLint durante el build de producción
    ignoreDuringBuilds: true,
  },
  typescript: {
    // Deshabilitar errores de TypeScript durante el build
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
