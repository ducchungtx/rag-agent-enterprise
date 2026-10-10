import { Link } from "react-router-dom";

interface Props {
  reason: string;
  suggestedMessage?: string | null;
  onChangeKb?: () => void;
}

export function RefusalBanner({ reason, suggestedMessage, onChangeKb }: Props) {
  return (
    <div className="rounded-[12px] border border-outline-variant border-l-[3px] border-l-warn bg-surface-lowest p-4 shadow-sm">
      <div className="flex items-start gap-3">
        <span className="material-symbols-outlined text-warn">warning</span>
        <div className="min-w-0 flex-1">
          <h3 className="font-display text-base font-bold text-warn">
            Không đủ nguồn phù hợp
          </h3>
          <p className="mt-1 text-sm text-on-surface-variant">{reason}</p>
          {suggestedMessage && (
            <p className="mt-2 text-sm text-on-surface">{suggestedMessage}</p>
          )}
          <div className="mt-3 flex flex-wrap gap-2">
            <button
              type="button"
              onClick={onChangeKb}
              className="rounded-[10px] bg-primary px-3 py-1.5 text-sm font-semibold text-on-primary"
            >
              Đổi KB
            </button>
            <Link
              to="/knowledge"
              className="rounded-[10px] border border-outline-variant px-3 py-1.5 text-sm font-semibold hover:border-primary-container"
            >
              Xem kho tri thức
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
