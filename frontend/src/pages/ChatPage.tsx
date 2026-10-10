import { useMemo, useState } from "react";
import { api } from "../api/client";
import type { ChatOut, CitationOut } from "../api/types";
import { useAuth } from "../auth/AuthContext";
import { CitationPanel } from "../components/CitationPanel";
import { RefusalBanner } from "../components/RefusalBanner";
import { ScopeBar } from "../components/ScopeBar";

type Mode = "chat" | "agent";

export function ChatPage() {
  const { token, tenantId, kbId, kbs, setKbId, setStatus } = useAuth();
  const [question, setQuestion] = useState("");
  const [busy, setBusy] = useState(false);
  const [answer, setAnswer] = useState("");
  const [citations, setCitations] = useState<CitationOut[]>([]);
  const [refused, setRefused] = useState(false);
  const [refusalReason, setRefusalReason] = useState("");
  const [suggested, setSuggested] = useState<string | null>(null);
  const [events, setEvents] = useState<string[]>([]);
  const [showKbPicker, setShowKbPicker] = useState(false);

  const kbName = useMemo(() => kbs.find((k) => k.id === kbId)?.name, [kbs, kbId]);

  const resetResult = () => {
    setAnswer("");
    setCitations([]);
    setRefused(false);
    setRefusalReason("");
    setSuggested(null);
    setEvents([]);
  };

  const runChat = async () => {
    if (!kbId) {
      setStatus("Chọn KB trước khi chat.", "warn");
      return;
    }
    setBusy(true);
    resetResult();
    try {
      const out = await api<ChatOut>(
        "/chat",
        {
          method: "POST",
          body: JSON.stringify({ question, kb_id: kbId, top_k: 5 }),
        },
        token,
        tenantId,
      );
      if (out.refused) {
        setRefused(true);
        setRefusalReason(
          out.refusal_reason ||
            `Không đủ nguồn phù hợp trong KB «${kbName || kbId}».`,
        );
        setSuggested(out.suggested_message ?? null);
        setCitations(out.citations || []);
      } else {
        setAnswer(out.answer);
        setCitations(out.citations || []);
      }
    } catch (err) {
      setStatus(err instanceof Error ? err.message : "Chat lỗi", "error");
    } finally {
      setBusy(false);
    }
  };

  const runAgent = async () => {
    if (!kbId) {
      setStatus("Chọn KB trước khi agent.", "warn");
      return;
    }
    setBusy(true);
    resetResult();
    const lines: string[] = [];
    let buffer = "";
    let wasRefused = false;
    try {
      const res = await fetch("/agent/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          "X-Tenant-Id": tenantId,
        },
        body: JSON.stringify({ question, kb_id: kbId, max_steps: 5 }),
      });
      if (!res.ok || !res.body) {
        throw new Error(`Agent HTTP ${res.status}`);
      }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let finalAnswer = "";

      const handleBlock = (block: string) => {
        const blockLines = block.split("\n");
        let event = "message";
        let data = "";
        for (const line of blockLines) {
          if (line.startsWith("event:")) event = line.slice(6).trim();
          else if (line.startsWith("data:")) data += line.slice(5).trim();
        }
        if (!data) return;
        let payload: Record<string, unknown> = {};
        try {
          payload = JSON.parse(data) as Record<string, unknown>;
        } catch {
          payload = { raw: data };
        }
        lines.push(`${event}: ${JSON.stringify(payload)}`);
        if (event === "token" && typeof payload.text === "string") {
          finalAnswer += payload.text;
        }
        if (event === "done") {
          if (payload.refused) {
            wasRefused = true;
            setRefused(true);
            setRefusalReason(
              String(
                payload.refusal_reason ||
                  `Agent không tìm thấy nguồn phù hợp trong KB «${kbName || kbId}».`,
              ),
            );
            if (typeof payload.suggested_message === "string") {
              setSuggested(payload.suggested_message);
            }
          }
          if (typeof payload.answer === "string") finalAnswer = payload.answer;
          if (Array.isArray(payload.citations)) {
            setCitations(payload.citations as CitationOut[]);
          }
        }
      };

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop() || "";
        for (const part of parts) handleBlock(part);
      }
      if (buffer.trim()) handleBlock(buffer);
      setEvents(lines);
      if (!wasRefused && finalAnswer) setAnswer(finalAnswer);
    } catch (err) {
      setStatus(err instanceof Error ? err.message : "Agent lỗi", "error");
    } finally {
      setBusy(false);
    }
  };

  const submit = (mode: Mode) => {
    if (!question.trim()) return;
    void (mode === "chat" ? runChat() : runAgent());
  };

  return (
    <div>
      <ScopeBar onChangeKb={() => setShowKbPicker(true)} />

      {showKbPicker && (
        <div className="mb-4 rounded-[12px] border border-outline-variant bg-surface-lowest p-4">
          <div className="mb-2 flex items-center justify-between">
            <h3 className="font-semibold">Chọn Knowledge Base</h3>
            <button type="button" className="text-sm text-on-surface-variant" onClick={() => setShowKbPicker(false)}>
              Đóng
            </button>
          </div>
          <div className="grid gap-2 md:grid-cols-2">
            {kbs.map((k) => (
              <button
                key={k.id}
                type="button"
                onClick={() => {
                  setKbId(k.id);
                  setShowKbPicker(false);
                }}
                className={`rounded-[10px] border p-3 text-left ${
                  k.id === kbId
                    ? "border-primary-container bg-secondary-container/30"
                    : "border-outline-variant hover:border-primary-container"
                }`}
              >
                <div className="font-semibold">{k.name}</div>
                <div className="mt-1 text-sm text-on-surface-variant">
                  {k.description || "Không mô tả"}
                </div>
              </button>
            ))}
            {!kbs.length && (
              <p className="text-sm text-on-surface-variant">Chưa có KB — vào Kho tri thức để tạo.</p>
            )}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-12">
        <section className="flex flex-col gap-4 xl:col-span-7">
          {refused && (
            <RefusalBanner
              reason={refusalReason}
              suggestedMessage={suggested}
              onChangeKb={() => setShowKbPicker(true)}
            />
          )}

          {!refused && answer && (
            <article className="rounded-[12px] border border-outline-variant bg-surface-lowest p-4 shadow-sm">
              <h2 className="font-display text-lg font-bold">Trả lời</h2>
              <pre className="mt-2 whitespace-pre-wrap font-body text-sm leading-relaxed">
                {answer}
              </pre>
            </article>
          )}

          {events.length > 0 && (
            <details className="rounded-[12px] border border-outline-variant bg-surface-low p-3 text-sm">
              <summary className="cursor-pointer font-semibold">Agent events</summary>
              <ul className="mt-2 max-h-48 list-disc overflow-auto pl-5 text-on-surface-variant">
                {events.map((e, i) => (
                  <li key={i} className="break-all">
                    {e}
                  </li>
                ))}
              </ul>
            </details>
          )}

          <form
            className="rounded-[12px] border border-outline-variant bg-surface-lowest p-4 shadow-sm"
            onSubmit={(e) => {
              e.preventDefault();
              submit("chat");
            }}
          >
            <label className="text-sm font-semibold">
              Câu hỏi
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                rows={3}
                required
                disabled={busy || !kbId}
                placeholder="Thời hạn sử dụng đất nông nghiệp của cá nhân trực tiếp sản xuất là bao lâu?"
                className="mt-2 w-full rounded-[10px] border border-outline-variant bg-surface px-3 py-2 outline-none focus:border-primary-container disabled:opacity-60"
              />
            </label>
            <div className="mt-3 flex flex-wrap gap-2">
              <button
                type="submit"
                disabled={busy || !kbId}
                className="rounded-[10px] bg-primary px-4 py-2 text-sm font-semibold text-on-primary disabled:opacity-60"
              >
                {busy ? "Đang xử lý…" : "Chat"}
              </button>
              <button
                type="button"
                disabled={busy || !kbId}
                onClick={() => submit("agent")}
                className="rounded-[10px] border border-outline-variant bg-surface px-4 py-2 text-sm font-semibold hover:border-primary-container disabled:opacity-60"
              >
                Agent (SSE)
              </button>
            </div>
          </form>
        </section>

        <aside className="xl:col-span-5">
          <CitationPanel citations={citations} />
        </aside>
      </div>
    </div>
  );
}
