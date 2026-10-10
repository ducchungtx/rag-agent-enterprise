const STORAGE = {
  token: "rae_token",
  tenantId: "rae_tenant_id",
  kbId: "rae_kb_id",
} as const;

export function getStoredToken(): string {
  return localStorage.getItem(STORAGE.token) || "";
}

export function getStoredTenantId(): string {
  return localStorage.getItem(STORAGE.tenantId) || "";
}

export function getStoredKbId(): string {
  return localStorage.getItem(STORAGE.kbId) || "";
}

export function setStoredToken(token: string) {
  if (token) localStorage.setItem(STORAGE.token, token);
  else localStorage.removeItem(STORAGE.token);
}

export function setStoredTenantId(id: string) {
  if (id) localStorage.setItem(STORAGE.tenantId, id);
  else localStorage.removeItem(STORAGE.tenantId);
}

export function setStoredKbId(id: string) {
  if (id) localStorage.setItem(STORAGE.kbId, id);
  else localStorage.removeItem(STORAGE.kbId);
}

export function clearSessionStorage() {
  localStorage.removeItem(STORAGE.token);
  localStorage.removeItem(STORAGE.tenantId);
  localStorage.removeItem(STORAGE.kbId);
}

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export function authHeaders(
  token: string,
  tenantId: string,
  json = true,
): HeadersInit {
  const h: Record<string, string> = {};
  if (json) h["Content-Type"] = "application/json";
  if (token) h.Authorization = `Bearer ${token}`;
  if (tenantId) h["X-Tenant-Id"] = tenantId;
  return h;
}

export async function api<T>(
  path: string,
  options: RequestInit = {},
  token = getStoredToken(),
  tenantId = getStoredTenantId(),
): Promise<T> {
  const headers = new Headers(options.headers);
  const isForm = typeof FormData !== "undefined" && options.body instanceof FormData;
  if (!headers.has("Content-Type") && options.body && !isForm) {
    headers.set("Content-Type", "application/json");
  }
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (tenantId) headers.set("X-Tenant-Id", tenantId);

  const res = await fetch(path, { ...options, headers });
  const text = await res.text();
  let data: unknown = null;
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }
  if (!res.ok) {
    const detail =
      data &&
      typeof data === "object" &&
      data !== null &&
      ("detail" in data || "message" in data)
        ? String(
            (data as { detail?: unknown; message?: unknown }).detail ??
              (data as { message?: unknown }).message,
          )
        : typeof data === "string"
          ? data
          : res.statusText;
    throw new ApiError(detail, res.status);
  }
  return data as T;
}
