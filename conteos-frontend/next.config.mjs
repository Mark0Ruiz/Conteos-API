/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    // ⚠ Permite que el build termine aunque haya errores de ESLint
    ignoreDuringBuilds: true,
  },
  typescript: {
    // ⚠ Permite que el build termine aunque haya errores de TypeScript
    ignoreBuildErrors: true,
  },
};

export default nextConfig;

