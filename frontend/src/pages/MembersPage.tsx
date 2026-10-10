import { useEffect, useState } from "react";
import { api } from "../api/client";
import type { MemberOut } from "../api/types";
import { useAuth } from "../auth/AuthContext";

export function MembersPage() {
  const { token, tenantId, setStatus } = useAuth();
  const [members, setMembers] = useState<MemberOut[]>([]);

  useEffect(() => {
    if (!tenantId) return;
    void api<MemberOut[]>(`/tenants/${tenantId}/members`, {}, token, tenantId)
      .then(setMembers)
      .catch((err: Error) => setStatus(err.message, "error"));
  }, [tenantId, token, setStatus]);

  return (
    <div>
      <h1 className="font-display text-2xl font-bold">Thành viên & phân quyền</h1>
      <p className="mt-1 text-sm text-on-surface-variant">
        RBAC trong workspace hiện tại (wireframe chức năng).
      </p>
      <div className="mt-4 overflow-hidden rounded-[12px] border border-outline-variant bg-surface-lowest">
        <table className="w-full text-left text-sm">
          <thead className="bg-surface-low text-xs uppercase tracking-wide text-on-surface-variant">
            <tr>
              <th className="px-4 py-3">User</th>
              <th className="px-4 py-3">Email</th>
              <th className="px-4 py-3">Role</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody>
            {members.map((m) => (
              <tr key={m.user_id} className="border-t border-outline-variant/60">
                <td className="px-4 py-3 font-medium">{m.username}</td>
                <td className="px-4 py-3">{m.email}</td>
                <td className="px-4 py-3">
                  <span className="rounded bg-secondary-container/50 px-1.5 py-0.5 text-[11px] font-bold uppercase">
                    {m.role}
                  </span>
                </td>
                <td className="px-4 py-3">{m.status}</td>
              </tr>
            ))}
            {!members.length && (
              <tr>
                <td colSpan={4} className="px-4 py-6 text-on-surface-variant">
                  Chưa có dữ liệu / chưa chọn workspace.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
