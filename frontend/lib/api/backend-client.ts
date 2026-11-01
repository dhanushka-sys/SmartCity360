let cachedBaseUrl: string | null = null;

const DEFAULT_BASE_URLS = [
  "http://localhost:8080/api",
  "http://localhost:8080/smartcity360-backend/api",
];

export const BACKEND_BASE_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8080/api";

export async function resolveBackendBaseUrl(): Promise<string> {
  if (process.env.NEXT_PUBLIC_BACKEND_URL) {
    return process.env.NEXT_PUBLIC_BACKEND_URL;
  }
  if (cachedBaseUrl) {
    return cachedBaseUrl;
  }

  for (const candidate of DEFAULT_BASE_URLS) {
    try {
      const res = await fetch(`${candidate}/dashboard`, {
        method: "GET",
        signal: AbortSignal.timeout(1200),
      });
      if (res.status !== 404) {
        cachedBaseUrl = candidate;
        return candidate;
      }
    } catch {
      // Continue checking next candidate
    }
  }

  return DEFAULT_BASE_URLS[0];
}

export async function fetchFromBackend<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const cleanEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  const baseUrl = await resolveBackendBaseUrl();
  const url = `${baseUrl}${cleanEndpoint}`;

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    const res = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers || {}),
      },
    });

    clearTimeout(timeoutId);

    if (!res.ok) {
      let errMsg = `Request failed with status ${res.status}`;
      try {
        const errJson = await res.json();
        if (errJson && errJson.error) {
          errMsg = errJson.error;
        }
      } catch {
        // Ignored
      }
      throw new Error(errMsg);
    }

    return (await res.json()) as T;
  } catch (err: unknown) {
    if (err instanceof Error) {
      if (
        err.name === "AbortError" ||
        err.message.includes("Failed to fetch") ||
        err.message.includes("NetworkError")
      ) {
        throw new Error(
          `Unable to connect to Tomcat 9 backend at ${baseUrl}. Ensure your Apache Tomcat 9 server is running in IntelliJ.`
        );
      }
      throw err;
    }
    throw new Error(`Connection error connecting to ${url}`);
  }
}

export async function checkBackendConnection(): Promise<boolean> {
  try {
    const baseUrl = await resolveBackendBaseUrl();
    const res = await fetch(`${baseUrl}/dashboard`, {
      method: "GET",
      signal: AbortSignal.timeout(1800),
    });
    return res.status === 200;
  } catch {
    return false;
  }
}
