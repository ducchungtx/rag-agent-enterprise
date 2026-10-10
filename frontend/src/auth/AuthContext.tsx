import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  api,
  ApiError,
  clearSessionStorage,
  getStoredKbId,
  getStoredTenantId,
  getStoredToken,
  setStoredKbId,
  setStoredTenantId,
  setStoredToken,
} from "../api/client";
import type { KBOut, TenantOut, TokenOut, UserOut } from "../api/types";

interface AuthState {
  token: string;
  tenantId: string;
  kbId: string;
  user: UserOut | null;
  tenants: TenantOut[];
  kbs: KBOut[];
  loading: boolean;
  status: string;
  statusKind: "" | "error" | "warn";
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, username: string) => Promise<void>;
  logout: () => void;
  setTenantId: (id: string) => Promise<void>;
  setKbId: (id: string) => void;
  createTenant: (name: string) => Promise<void>;
  createKb: (name: string, description: string) => Promise<KBOut>;
  refreshKbs: () => Promise<KBOut[]>;
  setStatus: (msg: string, kind?: "" | "error" | "warn") => void;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState(getStoredToken);
  const [tenantId, setTenantIdState] = useState(getStoredTenantId);
  const [kbId, setKbIdState] = useState(getStoredKbId);
  const [user, setUser] = useState<UserOut | null>(null);
  const [tenants, setTenants] = useState<TenantOut[]>([]);
  const [kbs, setKbs] = useState<KBOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [status, setStatusMsg] = useState("");
  const [statusKind, setStatusKind] = useState<"" | "error" | "warn">("");

  const setStatus = useCallback((msg: string, kind: "" | "error" | "warn" = "") => {
    setStatusMsg(msg);
    setStatusKind(kind);
  }, []);

  const logout = useCallback(() => {
    setToken("");
    setTenantIdState("");
    setKbIdState("");
    setUser(null);
    setTenants([]);
    setKbs([]);
    clearSessionStorage();
    setStatus("Đã đăng xuất.");
  }, [setStatus]);

  const loadKbs = useCallback(
    async (tok: string, tid: string): Promise<KBOut[]> => {
      if (!tok || !tid) {
        setKbs([]);
        return [];
      }
      const list = await api<KBOut[]>("/kb", {}, tok, tid);
      setKbs(list);
      const current = getStoredKbId();
      if (!list.length) {
        setKbIdState("");
        setStoredKbId("");
      } else if (!current || !list.some((k) => k.id === current)) {
        setKbIdState(list[0].id);
        setStoredKbId(list[0].id);
      } else {
        setKbIdState(current);
      }
      return list;
    },
    [],
  );

  const loadTenants = useCallback(
    async (tok: string) => {
      const list = await api<TenantOut[]>("/tenants", {}, tok, "");
      setTenants(list);
      let tid = getStoredTenantId();
      if (tid && !list.some((t) => t.id === tid)) {
        tid = "";
        setStoredTenantId("");
        setStoredKbId("");
        setKbIdState("");
      }
      if (!tid && list[0]) {
        tid = list[0].id;
        setStoredTenantId(tid);
      }
      setTenantIdState(tid);
      if (tid) await loadKbs(tok, tid);
      else setKbs([]);
      return list;
    },
    [loadKbs],
  );

  const refreshSession = useCallback(async () => {
    const tok = getStoredToken();
    if (!tok) {
      setLoading(false);
      return;
    }
    setToken(tok);
    try {
      const me = await api<UserOut>("/auth/me", {}, tok, "");
      setUser(me);
      await loadTenants(tok);
      setStatus("Sẵn sàng.");
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        logout();
        setStatus("Phiên hết hạn — đăng nhập lại.", "error");
      } else {
        setStatus(err instanceof Error ? err.message : "Lỗi phiên", "error");
      }
    } finally {
      setLoading(false);
    }
  }, [loadTenants, logout, setStatus]);

  useEffect(() => {
    void refreshSession();
  }, [refreshSession]);

  const applyToken = async (access: string) => {
    setStoredToken(access);
    setToken(access);
    setLoading(true);
    await refreshSession();
  };

  const login = async (email: string, password: string) => {
    const out = await api<TokenOut>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }, "", "");
    await applyToken(out.access_token);
  };

  const register = async (email: string, password: string, username: string) => {
    const out = await api<TokenOut>("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        email,
        password,
        username: username || email.split("@")[0],
      }),
    }, "", "");
    await applyToken(out.access_token);
  };

  const setTenantId = async (id: string) => {
    setTenantIdState(id);
    setStoredTenantId(id);
    setKbIdState("");
    setStoredKbId("");
    if (token && id) {
      await loadKbs(token, id);
      setStatus(`Workspace đã chọn.`);
    }
  };

  const setKbId = (id: string) => {
    setKbIdState(id);
    setStoredKbId(id);
  };

  const createTenant = async (name: string) => {
    const t = await api<TenantOut>(
      "/tenants",
      { method: "POST", body: JSON.stringify({ name }) },
      token,
      "",
    );
    await loadTenants(token);
    await setTenantId(t.id);
  };

  const createKb = async (name: string, description: string) => {
    const kb = await api<KBOut>(
      "/kb",
      { method: "POST", body: JSON.stringify({ name, description }) },
      token,
      tenantId,
    );
    const list = await loadKbs(token, tenantId);
    setKbId(kb.id);
    return list.find((k) => k.id === kb.id) ?? kb;
  };

  const refreshKbs = async () => loadKbs(token, tenantId);

  const value = useMemo<AuthState>(
    () => ({
      token,
      tenantId,
      kbId,
      user,
      tenants,
      kbs,
      loading,
      status,
      statusKind,
      login,
      register,
      logout,
      setTenantId,
      setKbId,
      createTenant,
      createKb,
      refreshKbs,
      setStatus,
    }),
    [
      token,
      tenantId,
      kbId,
      user,
      tenants,
      kbs,
      loading,
      status,
      statusKind,
      logout,
      setStatus,
    ],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth outside AuthProvider");
  return ctx;
}
