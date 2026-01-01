const path = require('path')

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'export', // Static export for FastAPI to serve
  // No rewrites needed in unified deployment - FastAPI handles routing
  images: {
    unoptimized: true, // Required for static export
  },
  
  webpack: (config) => {
    // Ensure @ alias resolves correctly
    const alias = config.resolve.alias || {}
    alias['@'] = path.join(__dirname)
    config.resolve.alias = alias
    return config
  },
}

module.exports = nextConfig

