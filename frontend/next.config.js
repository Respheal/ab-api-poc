/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    env: {
        API_BASE_PATH: process.env.API_BASE_PATH,
    },
};

module.exports = nextConfig;
