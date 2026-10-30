/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  webpack: (config, { dev }) => {
    if (dev) {
      // Prevents Windows PackFileCacheStrategy ENOENT file locking crash in .next/cache
      config.cache = false;
    }
    return config;
  },
};

export default nextConfig;

