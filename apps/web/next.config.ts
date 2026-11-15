import type { NextConfig } from "next";
const config: NextConfig = {
  experimental: { cpus: 1 },
  poweredByHeader: false,
  async rewrites() {
    return [
      {
        source: "/v1/:path*",
        destination: `${process.env.API_ORIGIN || "http://127.0.0.1:8000"}/v1/:path*`,
      },
    ];
  },
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "X-Frame-Options", value: "DENY" },
        ],
      },
    ];
  },
};
export default config;
