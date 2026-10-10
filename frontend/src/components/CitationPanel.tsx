import type { CitationOut } from "../api/types";

export function CitationPanel({ citations }: { citations: CitationOut[] }) {
  if (!citations.length) {
    return (
      <div className="rounded-[12px] border border-outline-variant bg-surface-lowest p-4 text-sm text-on-surface-variant">
        Chưa có citation.
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      <h2 className="font-display text-lg font-bold">Citations</h2>
      {citations.map((c, i) => (
        <article
          key={c.chunk_id}
          className="rounded-[12px] border border-outline-variant border-l-[3px] border-l-primary-container bg-surface-lowest p-3 shadow-sm"
        >
          <div className="mb-1 flex items-center justify-between gap-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-primary">
              [{i + 1}] {c.title}
            </span>
            <span className="text-[11px] text-on-surface-variant">
              score {c.score.toFixed(2)}
            </span>
          </div>
          <p className="text-sm leading-relaxed text-on-surface-variant">{c.content}</p>
        </article>
      ))}
    </div>
  );
}
