export const BACKEND_BASE_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8080/smartcity360-backend/api";

export async function fetchFromBackend<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T | null> {
  if (typeof window === "undefined") {
    return null;
  }

  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 2500);

    const cleanEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
    const url = `${BACKEND_BASE_URL}${cleanEndpoint}`;

    const res = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers || {}),
      },
    });

    clearTimeout(timeoutId);

    if (res.ok) {
      return (await res.json()) as T;
    }
  } catch {
    // Graceful fallback to simulated memory data when Tomcat is offline
  }

  return null;
}

export async function checkBackendConnection(): Promise<boolean> {
  try {
    const res = await fetch(`${BACKEND_BASE_URL}/zones`, {
      method: "GET",
      signal: AbortSignal.timeout(1500),
    });
    return res.ok;
  } catch {
    return false;
  }
}

