/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone', // Required for Docker/Cloud Run deployment
  // No rewrites needed in unified deployment - FastAPI handles routing
  // Next.js automatically uses tsconfig.json paths for alias resolution
}

module.exports = nextConfig

