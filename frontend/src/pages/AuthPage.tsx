import { useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export function AuthPage() {
  const { token, loading, login, register, setStatus } = useAuth();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [busy, setBusy] = useState(false);

  if (!loading && token) return <Navigate to="/chat" replace />;

  return (
    <div className="relative min-h-screen overflow-hidden bg-surface">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(900px_500px_at_10%_-10%,#cfe8e0_0%,transparent_55%),radial-gradient(700px_400px_at_100%_0%,#d7e2ea_0%,transparent_50%)]" />
      <div className="relative mx-auto flex min-h-screen max-w-6xl flex-col justify-center gap-10 px-6 py-12 lg:flex-row lg:items-center lg:gap-16">
        <section className="flex-1">
          <div className="mb-4 inline-grid h-14 w-14 place-items-center rounded-xl bg-primary font-display text-xl font-bold text-on-primary">
            rae
          </div>
          <h1 className="font-display text-4xl font-bold tracking-tight text-on-surface md:text-5xl">
            rae
          </h1>
          <p className="mt-2 text-lg text-on-surface-variant">
            Trợ lý pháp chế · có citation.
          </p>
          <p className="mt-6 max-w-md text-on-surface-variant">
            Hỏi trong đúng Workspace + đúng Knowledge Base, trả lời có trích dẫn,
            từ chối khi thiếu nguồn.
          </p>
          <ul className="mt-6 space-y-2 text-sm text-on-surface-variant">
            <li className="flex items-center gap-2">
              <span className="material-symbols-outlined text-primary text-[18px]">verified</span>
              Citations xác thực — không ảo giác
            </li>
            <li className="flex items-center gap-2">
              <span className="material-symbols-outlined text-primary text-[18px]">gavel</span>
              Phạm vi KB tường minh theo miền
            </li>
          </ul>
        </section>

        <section className="w-full max-w-md rounded-[12px] border border-outline-variant bg-surface-lowest p-6 shadow-[0_12px_32px_rgba(19,33,43,0.08)]">
          <h2 className="font-display text-xl font-bold">
            {mode === "login" ? "Đăng nhập chuyên viên" : "Đăng ký"}
          </h2>
          <form
            className="mt-4 flex flex-col gap-3"
            onSubmit={(e) => {
              e.preventDefault();
              const fd = new FormData(e.currentTarget);
              const email = String(fd.get("email") || "").trim();
              const password = String(fd.get("password") || "");
              const username = String(fd.get("username") || "").trim();
              setBusy(true);
              const run =
                mode === "login"
                  ? login(email, password)
                  : register(email, password, username);
              void run
                .catch((err: Error) => setStatus(err.message, "error"))
                .finally(() => setBusy(false));
            }}
          >
            <label className="text-sm">
              Email
              <input
                name="email"
                type="email"
                required
                autoComplete="username"
                className="mt-1 w-full rounded-[10px] border border-outline-variant bg-surface px-3 py-2 outline-none focus:border-primary-container"
              />
            </label>
            {mode === "register" && (
              <label className="text-sm">
                Username
                <input
                  name="username"
                  minLength={2}
                  autoComplete="nickname"
                  className="mt-1 w-full rounded-[10px] border border-outline-variant bg-surface px-3 py-2 outline-none focus:border-primary-container"
                />
              </label>
            )}
            <label className="text-sm">
              Password
              <input
                name="password"
                type="password"
                required
                minLength={8}
                autoComplete={mode === "login" ? "current-password" : "new-password"}
                className="mt-1 w-full rounded-[10px] border border-outline-variant bg-surface px-3 py-2 outline-none focus:border-primary-container"
              />
            </label>
            <div className="mt-2 flex gap-2">
              <button
                type="submit"
                disabled={busy}
                className="grow rounded-[10px] bg-primary px-4 py-2.5 font-semibold text-on-primary hover:bg-primary-container disabled:opacity-60"
                onClick={() => setMode("login")}
              >
                Đăng nhập
              </button>
              <button
                type="submit"
                disabled={busy}
                className="rounded-[10px] border border-outline-variant bg-surface px-4 py-2.5 font-semibold hover:border-primary-container"
                onClick={() => setMode("register")}
              >
                Đăng ký
              </button>
            </div>
          </form>
        </section>
      </div>
    </div>
  );
}
