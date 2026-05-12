import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  typescript: {
    // Deshabilitar errores de TypeScript durante el build
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
