/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    // ⚠ Permite que el build termine aunque haya errores de TypeScript
    ignoreBuildErrors: true,
  },
};

export default nextConfig;

