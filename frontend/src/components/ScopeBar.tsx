import { useAuth } from "../auth/AuthContext";

export function ScopeBar({ onChangeKb }: { onChangeKb?: () => void }) {
  const { kbs, kbId, tenants, tenantId } = useAuth();
  const kb = kbs.find((k) => k.id === kbId);
  const tenant = tenants.find((t) => t.id === tenantId);

  return (
    <div className="sticky top-16 z-30 -mx-6 mb-6 border-b border-outline-variant/40 bg-surface-lowest px-6 py-3 shadow-sm">
      <div className="flex flex-col justify-between gap-3 lg:flex-row lg:items-center">
        <div className="flex min-w-0 items-start gap-3 lg:items-center">
          <div className="flex shrink-0 items-center gap-2 rounded-lg bg-surface-low px-2 py-1">
            <span className="h-2.5 w-2.5 animate-pulse rounded-full bg-primary-container" />
            <span className="text-[11px] font-bold uppercase tracking-wider text-on-surface-variant">
              Scope Active
            </span>
          </div>
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2 text-sm">
              <span className="text-on-surface-variant">Đang hỏi trong:</span>
              <span className="font-semibold">{tenant?.name || "—"}</span>
              <span className="text-outline-variant">/</span>
              <span className="inline-flex items-center gap-1 rounded bg-secondary-container/40 px-2 py-0.5 font-bold text-primary">
                <span className="material-symbols-outlined text-[16px]">menu_book</span>
                {kb?.name || "Chưa chọn KB"}
              </span>
            </div>
            <p className="truncate text-sm text-on-surface-variant">
              {kb?.description ||
                (kb ? "Chưa có mô tả phạm vi — nên bổ sung khi tạo KB." : "Chọn KB để chat.")}
            </p>
          </div>
        </div>
        <button
          type="button"
          onClick={onChangeKb}
          className="inline-flex items-center gap-1.5 self-end rounded-lg bg-primary px-3 py-1.5 text-sm font-semibold text-on-primary hover:bg-primary-container lg:self-auto"
        >
          <span className="material-symbols-outlined text-[18px]">swap_horiz</span>
          Đổi KB
        </button>
      </div>
    </div>
  );
}
