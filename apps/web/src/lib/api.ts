export class ApiError extends Error {
  constructor(
    public code: string,
    message: string,
    public status: number,
    public fields: Record<string, string> = {},
  ) {
    super(message);
  }
}
export async function api<T = Record<string, unknown>>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const method = options.method || "GET";
  let csrf = "";
  if (!["GET", "HEAD"].includes(method)) {
    const res = await fetch("/v1/auth/csrf", {
      credentials: "same-origin",
      cache: "no-store",
    });
    csrf = (await res.json()).csrf_token;
  }
  const res = await fetch("/v1" + path, {
    ...options,
    credentials: "same-origin",
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
      ...(csrf ? { "X-CSRFToken": csrf } : {}),
      ...options.headers,
    },
  });
  const data =
    res.status === 204
      ? {}
      : res.headers.get("content-type")?.includes("application/json")
        ? await res.json()
        : {
            message:
              "The server could not complete this request. Refresh and try again.",
          };
  if (!res.ok)
    throw new ApiError(
      data.code || "request_failed",
      data.message || "We could not load this information.",
      res.status,
      data.fields,
    );
  return data as T;
}
export function money(amount: number, currency = "EUR") {
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(amount / 100);
}
export function label(value: string) {
  return value
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}
