import type { MetadataRoute } from "next";
export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: "*",
      disallow: ["/account", "/ops", "/dealer/", "/sign-in", "/v1/"],
      allow: "/",
    },
  };
}
