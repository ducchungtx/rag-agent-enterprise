import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

const nav = [
  { to: "/chat", label: "Hỏi đáp (Chat)" },
  { to: "/knowledge", label: "Kho tri thức" },
  { to: "/members", label: "Thành viên" },
  { to: "/api-keys", label: "Khóa API" },
];

export function AppShell() {
  const { user, tenants, tenantId, setTenantId, logout, status, statusKind, createTenant } =
    useAuth();

  return (
    <div className="min-h-screen bg-surface text-on-surface">
      <header className="sticky top-0 z-50 border-b border-outline-variant/40 bg-surface/95 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-[1440px] items-center justify-between gap-4 px-6">
          <div className="flex min-w-0 items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="grid h-9 w-9 place-items-center rounded-[10px] bg-primary font-display text-sm font-bold text-on-primary">
                rae
              </div>
              <div className="leading-tight">
                <div className="font-display text-lg font-bold">rae</div>
                <div className="text-[11px] font-semibold uppercase tracking-wider text-on-surface-variant">
                  Trợ lý pháp chế · có citation
                </div>
              </div>
            </div>
            <div className="hidden h-6 w-px bg-outline-variant/60 sm:block" />
            <label className="hidden items-center gap-2 rounded-lg bg-surface-low px-2 py-1 sm:flex">
              <span className="material-symbols-outlined text-[18px] text-primary">
                account_balance
              </span>
              <select
                className="max-w-[200px] border-0 bg-transparent text-sm font-semibold outline-none"
                value={tenantId}
                onChange={(e) => void setTenantId(e.target.value)}
              >
                {tenants.length === 0 && <option value="">(chưa có workspace)</option>}
                {tenants.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.name}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <nav className="hidden items-center gap-1 xl:flex">
            {nav.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `rounded-lg px-3 py-1.5 text-sm transition-colors ${
                    isActive
                      ? "bg-primary-container font-semibold text-on-primary"
                      : "text-on-surface-variant hover:bg-surface-container hover:text-on-surface"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div className="flex items-center gap-3">
            <div className="hidden rounded-lg bg-surface-lowest px-2 py-1 shadow-sm md:block">
              <div className="text-xs font-medium leading-none">{user?.email}</div>
              <div className="mt-1 text-[10px] font-bold uppercase tracking-wider text-on-secondary-container">
                Member
              </div>
            </div>
            <button
              type="button"
              title="Đăng xuất"
              className="rounded-lg p-1.5 text-on-surface-variant hover:bg-error-container/40 hover:text-error"
              onClick={logout}
            >
              <span className="material-symbols-outlined text-[20px]">logout</span>
            </button>
          </div>
        </div>
        {!tenantId && (
          <div className="border-t border-outline-variant/30 bg-surface-low px-6 py-2">
            <form
              className="mx-auto flex max-w-[1440px] flex-wrap items-end gap-2"
              onSubmit={(e) => {
                e.preventDefault();
                const fd = new FormData(e.currentTarget);
                const name = String(fd.get("name") || "").trim();
                if (name.length >= 2) void createTenant(name).then(() => e.currentTarget.reset());
              }}
            >
              <label className="grow text-sm">
                Tạo workspace
                <input
                  name="name"
                  minLength={2}
                  required
                  placeholder="Phòng Pháp chế"
                  className="mt-1 w-full rounded-[10px] border border-outline-variant bg-surface-lowest px-3 py-2"
                />
              </label>
              <button
                type="submit"
                className="rounded-[10px] bg-primary px-4 py-2 text-sm font-semibold text-on-primary"
              >
                Tạo
              </button>
            </form>
          </div>
        )}
      </header>

      <main className="mx-auto max-w-[1440px] px-6 py-6">
        <Outlet />
      </main>

      {status && (
        <aside
          className={`fixed bottom-4 right-4 max-w-sm rounded-[10px] border px-3 py-2 text-sm shadow-lg ${
            statusKind === "error"
              ? "border-error/30 bg-error-container text-error"
              : statusKind === "warn"
                ? "border-warn/40 bg-surface-lowest text-warn"
                : "border-outline-variant bg-surface-lowest text-on-surface"
          }`}
        >
          {status}
        </aside>
      )}
    </div>
  );
}
