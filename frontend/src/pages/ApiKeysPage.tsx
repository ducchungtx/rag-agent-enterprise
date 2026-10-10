import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { APIKeyOut } from "../api/types";
import { useAuth } from "../auth/AuthContext";

export function ApiKeysPage() {
  const { token, tenantId, setStatus } = useAuth();
  const [keys, setKeys] = useState<APIKeyOut[]>([]);

  useEffect(() => {
    if (!tenantId) return;
    void api<APIKeyOut[]>("/api-keys", {}, token, tenantId)
      .then(setKeys)
      .catch((err: Error) => setStatus(err.message, "error"));
  }, [tenantId, token, setStatus]);

  return (
    <div>
      <h1 className="font-display text-2xl font-bold">Khóa API doanh nghiệp</h1>
      <p className="mt-1 text-sm text-on-surface-variant">
        Capabilities + kb allowlist — danh sách read-only từ API hiện có.
      </p>
      <div className="mt-4 grid gap-3">
        {keys.map((k) => (
          <article
            key={k.id}
            className="rounded-[12px] border border-outline-variant bg-surface-lowest p-4"
          >
            <div className="flex flex-wrap items-center justify-between gap-2">
              <h2 className="font-semibold">{k.name}</h2>
              <code className="text-xs text-on-surface-variant">{k.key_prefix}…</code>
            </div>
            <div className="mt-2 flex flex-wrap gap-1">
              {k.capabilities.map((c) => (
                <span
                  key={c}
                  className="rounded bg-surface-high px-1.5 py-0.5 text-[11px] font-bold uppercase tracking-wide"
                >
                  {c}
                </span>
              ))}
            </div>
          </article>
        ))}
        {!keys.length && (
          <p className="text-sm text-on-surface-variant">Chưa có API key trong workspace.</p>
        )}
      </div>
    </div>
  );
}
