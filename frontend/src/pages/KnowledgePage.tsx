import { useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";
import type { DocumentOut } from "../api/types";
import { useAuth } from "../auth/AuthContext";

export function KnowledgePage() {
  const {
    token,
    tenantId,
    kbId,
    kbs,
    setKbId,
    createKb,
    refreshKbs,
    setStatus,
  } = useAuth();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [lastDoc, setLastDoc] = useState<DocumentOut | null>(null);
  const [busy, setBusy] = useState(false);

  const selected = kbs.find((k) => k.id === kbId);

  return (
    <div className="flex flex-col gap-6">
      <header>
        <h1 className="font-display text-2xl font-bold">Kho tri thức (Knowledge Bases)</h1>
        <p className="mt-1 text-sm text-on-surface-variant">
          Một KB ≈ một miền. Không trộn đất đai với hôn nhân gia đình.
        </p>
      </header>

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {kbs.map((k) => (
          <button
            key={k.id}
            type="button"
            onClick={() => setKbId(k.id)}
            className={`rounded-[12px] border p-4 text-left shadow-sm transition-colors ${
              k.id === kbId
                ? "border-primary-container bg-secondary-container/25"
                : "border-outline-variant bg-surface-lowest hover:border-primary-container"
            }`}
          >
            <div className="font-display text-lg font-bold">{k.name}</div>
            <p className="mt-2 line-clamp-3 text-sm text-on-surface-variant">
              {k.description || "Chưa có mô tả phạm vi"}
            </p>
            <div className="mt-3 flex gap-2">
              <Link
                to="/chat"
                onClick={() => setKbId(k.id)}
                className="text-sm font-semibold text-primary hover:underline"
              >
                Dùng để chat →
              </Link>
            </div>
          </button>
        ))}
        {!kbs.length && (
          <p className="text-sm text-on-surface-variant">Chưa có KB trong workspace này.</p>
        )}
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <form
          className="rounded-[12px] border border-outline-variant bg-surface-lowest p-4"
          onSubmit={(e) => {
            e.preventDefault();
            setBusy(true);
            void createKb(name, description)
              .then(() => {
                setName("");
                setDescription("");
                setStatus("Đã tạo KB.");
              })
              .catch((err: Error) => setStatus(err.message, "error"))
              .finally(() => setBusy(false));
          }}
        >
          <h2 className="font-display text-lg font-bold">Tạo KB mới</h2>
          <label className="mt-3 block text-sm">
            Tên
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              minLength={1}
              placeholder="Luật Đất đai"
              className="mt-1 w-full rounded-[10px] border border-outline-variant px-3 py-2"
            />
          </label>
          <label className="mt-3 block text-sm">
            Mô tả phạm vi (nên ghi loại trừ)
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              placeholder="NĐ/TT đất đai; không gồm hôn nhân gia đình"
              className="mt-1 w-full rounded-[10px] border border-outline-variant px-3 py-2"
            />
          </label>
          <button
            type="submit"
            disabled={busy || !tenantId}
            className="mt-3 rounded-[10px] bg-primary px-4 py-2 text-sm font-semibold text-on-primary disabled:opacity-60"
          >
            Tạo KB
          </button>
        </form>

        <form
          className="rounded-[12px] border border-outline-variant bg-surface-lowest p-4"
          onSubmit={(e) => {
            e.preventDefault();
            if (!kbId) {
              setStatus("Chọn KB trước khi upload.", "warn");
              return;
            }
            const fd = new FormData(e.currentTarget);
            const file = fd.get("file");
            if (!(file instanceof File) || !file.size) return;
            const body = new FormData();
            body.append("file", file);
            setBusy(true);
            void api<DocumentOut>(
              `/kb/${kbId}/documents`,
              { method: "POST", body },
              token,
              tenantId,
            )
              .then((doc) => {
                setLastDoc(doc);
                setStatus(`Upload: ${doc.title} · ${doc.parse_status}`);
                return refreshKbs();
              })
              .catch((err: Error) => setStatus(err.message, "error"))
              .finally(() => {
                setBusy(false);
                e.currentTarget.reset();
              });
          }}
        >
          <h2 className="font-display text-lg font-bold">Upload vào KB đang chọn</h2>
          <p className="mt-1 text-sm text-on-surface-variant">
            Đích: <strong>{selected?.name || "—"}</strong>
          </p>
          <label className="mt-3 block text-sm">
            File (.md / .txt / .pdf)
            <input
              name="file"
              type="file"
              accept=".md,.txt,.pdf"
              required
              className="mt-1 block w-full text-sm"
            />
          </label>
          <button
            type="submit"
            disabled={busy || !kbId}
            className="mt-3 rounded-[10px] border border-outline-variant bg-surface px-4 py-2 text-sm font-semibold hover:border-primary-container disabled:opacity-60"
          >
            Upload
          </button>
          {lastDoc && (
            <p className="mt-3 text-sm text-on-surface-variant">
              Gần nhất: {lastDoc.title} · <code>{lastDoc.parse_status}</code>
              {lastDoc.error_message ? ` · ${lastDoc.error_message}` : ""}
            </p>
          )}
        </form>
      </section>
    </div>
  );
}
