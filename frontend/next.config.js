const path = require('path')

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone', // Required for Docker/Cloud Run deployment
  // No rewrites needed in unified deployment - FastAPI handles routing
  
  webpack: (config) => {
    // Ensure @ alias resolves correctly
    const alias = config.resolve.alias || {}
    alias['@'] = path.join(__dirname)
    config.resolve.alias = alias
    return config
  },
}

module.exports = nextConfig

