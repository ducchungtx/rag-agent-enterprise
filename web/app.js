(() => {
  const STORAGE = {
    token: "rae_token",
    tenantId: "rae_tenant_id",
    kbId: "rae_kb_id",
  };

  const state = {
    token: localStorage.getItem(STORAGE.token) || "",
    tenantId: localStorage.getItem(STORAGE.tenantId) || "",
    kbId: localStorage.getItem(STORAGE.kbId) || "",
    user: null,
    authMode: "login",
    chatMode: "chat",
    kbCount: 0,
  };

  const $ = (id) => document.getElementById(id);
  const statusEl = $("status");

  function setStatus(msg, kind = "") {
    statusEl.textContent = msg || "";
    statusEl.className = `status${kind ? ` ${kind}` : ""}`;
  }

  function headers(json = true) {
    const h = {};
    if (json) h["Content-Type"] = "application/json";
    if (state.token) h.Authorization = `Bearer ${state.token}`;
    if (state.tenantId) h["X-Tenant-Id"] = state.tenantId;
    return h;
  }

  async function api(path, options = {}) {
    const res = await fetch(path, options);
    const text = await res.text();
    let data = null;
    if (text) {
      try {
        data = JSON.parse(text);
      } catch {
        data = text;
      }
    }
    if (!res.ok) {
      const detail =
        (data && (data.detail || data.message)) ||
        (typeof data === "string" ? data : res.statusText);
      const err = new Error(
        typeof detail === "string" ? detail : JSON.stringify(detail),
      );
      err.status = res.status;
      throw err;
    }
    return data;
  }

  function showViews() {
    const authed = Boolean(state.token);
    const hasTenant = Boolean(state.tenantId);
    const hasKb = Boolean(state.kbId);

    $("view-auth").hidden = authed;
    $("view-workspace").hidden = !authed;
    $("view-kb").hidden = !(authed && hasTenant);
    // Chat hiện ngay khi đã chọn tenant — dùng KB cũ nếu có
    $("view-chat").hidden = !(authed && hasTenant);
    $("session-meta").hidden = !authed;

    const hint = $("kb-hint");
    if (authed && hasTenant && !hasKb) {
      hint.hidden = false;
      hint.textContent =
        state.kbCount === 0
          ? "Tenant này chưa có KB. Mở «Thêm KB / upload» bên dưới, hoặc chọn tenant đã demo trước đó."
          : "Chọn một KB trong danh sách để chat với dữ liệu đã ingest.";
    } else {
      hint.hidden = true;
    }

    const canChat = hasKb;
    $("btn-chat").disabled = !canChat;
    $("btn-agent").disabled = !canChat;
    $("chat-lede").textContent = canChat
      ? `Đang chat KB ${state.kbId.slice(0, 8)}… — dữ liệu đã ingest sẵn, không cần tạo KB mới.`
      : "Chọn KB có sẵn ở panel Knowledge để chat với dữ liệu cũ.";
  }

  async function refreshMe() {
    if (!state.token) {
      state.user = null;
      showViews();
      return;
    }
    // Giữ UI logged-in ngay khi có token (F5 không nhảy về form login)
    showViews();
    try {
      state.user = await api("/auth/me", { headers: headers() });
      $("user-label").textContent = `${state.user.username} · ${state.user.email}`;
    } catch (err) {
      // Chỉ xoá token khi JWT thật sự hết hạn / không hợp lệ
      if (err.status === 401) {
        logout(false);
        setStatus("Phiên hết hạn — đăng nhập lại.", "error");
      } else {
        setStatus(err.message || "Không tải được /auth/me.", "error");
        showViews();
      }
      return;
    }

    try {
      await loadTenants();
      if (state.tenantId) {
        await loadKbs();
      }
      showViews();
      if (state.kbId) {
        setStatus(`Sẵn sàng chat với KB cũ (${state.kbId.slice(0, 8)}…).`);
      } else if (state.tenantId) {
        setStatus("Đã đăng nhập — chọn KB có sẵn hoặc tạo mới nếu chưa có.");
      } else {
        setStatus("Đã đăng nhập — tạo hoặc chọn tenant.");
      }
    } catch (err) {
      // Lỗi tenant/KB không được đá ra khỏi phiên
      showViews();
      setStatus(err.message || "Không tải được tenant/KB.", "error");
    }
  }

  async function loadTenants() {
    const tenants = await api("/tenants", { headers: headers() });
    const sel = $("tenant-select");
    sel.innerHTML = "";
    if (!tenants.length) {
      sel.innerHTML = `<option value="">(chưa có tenant)</option>`;
      state.tenantId = "";
      state.kbId = "";
      localStorage.removeItem(STORAGE.tenantId);
      localStorage.removeItem(STORAGE.kbId);
      return;
    }

    const ids = new Set(tenants.map((t) => t.id));
    // localStorage trỏ tenant không thuộc user hiện tại → bỏ, lấy tenant đầu
    if (state.tenantId && !ids.has(state.tenantId)) {
      state.tenantId = "";
      state.kbId = "";
      localStorage.removeItem(STORAGE.tenantId);
      localStorage.removeItem(STORAGE.kbId);
    }

    for (const t of tenants) {
      const opt = document.createElement("option");
      opt.value = t.id;
      opt.textContent = `${t.name} (${t.id.slice(0, 8)}…)`;
      if (t.id === state.tenantId) opt.selected = true;
      sel.appendChild(opt);
    }

    if (!state.tenantId && tenants[0]) {
      state.tenantId = tenants[0].id;
      localStorage.setItem(STORAGE.tenantId, state.tenantId);
      sel.value = state.tenantId;
    }
  }

  async function loadKbs() {
    if (!state.tenantId) return;
    const kbs = await api("/kb", { headers: headers() });
    const sel = $("kb-select");
    sel.innerHTML = "";
    state.kbCount = kbs.length;

    if (!kbs.length) {
      sel.innerHTML = `<option value="">(chưa có KB)</option>`;
      state.kbId = "";
      localStorage.removeItem(STORAGE.kbId);
      showViews();
      return;
    }

    for (const k of kbs) {
      const opt = document.createElement("option");
      opt.value = k.id;
      opt.textContent = k.name;
      if (k.id === state.kbId) opt.selected = true;
      sel.appendChild(opt);
    }

    // Tự chọn KB đầu tiên nếu chưa có / KB cũ không còn trong list
    if (!state.kbId || !kbs.some((k) => k.id === state.kbId)) {
      state.kbId = kbs[0].id;
      localStorage.setItem(STORAGE.kbId, state.kbId);
      sel.value = state.kbId;
    }
    showViews();
  }

  async function selectTenant(id) {
    if (!id) {
      setStatus("Chưa có tenant — hãy tạo mới.", "warn");
      return;
    }
    state.tenantId = id;
    localStorage.setItem(STORAGE.tenantId, id);
    // Đổi tenant → bỏ kbId cũ (có thể thuộc tenant khác), load lại list
    state.kbId = "";
    localStorage.removeItem(STORAGE.kbId);
    try {
      await loadKbs();
      if (state.kbId) {
        setStatus(`Tenant ${id.slice(0, 8)}… · KB «${$("kb-select").selectedOptions[0]?.textContent || state.kbId.slice(0, 8)}» — có thể chat ngay.`);
      } else {
        setStatus(`Tenant ${id.slice(0, 8)}… chưa có KB.`, "warn");
      }
      showViews();
    } catch (err) {
      setStatus(err.message, "error");
    }
  }

  function logout(showMsg = true) {
    state.token = "";
    state.tenantId = "";
    state.kbId = "";
    state.user = null;
    state.kbCount = 0;
    localStorage.removeItem(STORAGE.token);
    localStorage.removeItem(STORAGE.tenantId);
    localStorage.removeItem(STORAGE.kbId);
    showViews();
    if (showMsg) setStatus("Đã đăng xuất.");
  }

  // --- Auth ---
  $("form-auth").addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-mode]");
    if (btn) state.authMode = btn.dataset.mode;
  });

  $("form-auth").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const email = String(fd.get("email") || "").trim();
    const password = String(fd.get("password") || "");
    const username = String(fd.get("username") || "").trim();
    try {
      setStatus(state.authMode === "register" ? "Đang đăng ký…" : "Đang đăng nhập…");
      const body =
        state.authMode === "register"
          ? { email, password, username: username || email.split("@")[0] }
          : { email, password };
      const path = state.authMode === "register" ? "/auth/register" : "/auth/login";
      const tokenOut = await api(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      state.token = tokenOut.access_token;
      localStorage.setItem(STORAGE.token, state.token);
      await refreshMe();
    } catch (err) {
      setStatus(err.message, "error");
    }
  });

  $("btn-logout").addEventListener("click", () => logout());

  // --- Tenant: đổi select là áp dụng ngay (không cần nút riêng) ---
  $("tenant-select").addEventListener("change", async () => {
    await selectTenant($("tenant-select").value);
  });

  $("form-tenant").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = String(new FormData(e.target).get("name") || "").trim();
    if (!name || name.length < 2) {
      setStatus("Nhập tên tenant (≥ 2 ký tự).", "warn");
      return;
    }
    try {
      setStatus("Đang tạo tenant…");
      const t = await api("/tenants", {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ name }),
      });
      e.target.reset();
      await loadTenants();
      await selectTenant(t.id);
      setStatus(`Đã tạo tenant «${t.name}».`);
    } catch (err) {
      setStatus(err.message, "error");
    }
  });

  // --- KB ---
  $("kb-select").addEventListener("change", () => {
    state.kbId = $("kb-select").value;
    if (state.kbId) {
      localStorage.setItem(STORAGE.kbId, state.kbId);
      setStatus(`Đang dùng KB «${$("kb-select").selectedOptions[0]?.textContent}» — chat được ngay.`);
    } else {
      localStorage.removeItem(STORAGE.kbId);
    }
    showViews();
  });

  $("form-kb").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = String(new FormData(e.target).get("name") || "").trim();
    if (!name) {
      setStatus("Nhập tên KB mới.", "warn");
      return;
    }
    try {
      setStatus("Đang tạo KB…");
      const kb = await api("/kb", {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ name, description: "" }),
      });
      state.kbId = kb.id;
      localStorage.setItem(STORAGE.kbId, kb.id);
      e.target.reset();
      await loadKbs();
      setStatus(`Đã tạo KB «${kb.name}».`);
    } catch (err) {
      setStatus(err.message, "error");
    }
  });

  $("form-upload").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!state.kbId) {
      setStatus("Chọn KB trước khi upload.", "warn");
      return;
    }
    const fileInput = e.target.querySelector('input[name="file"]');
    const file = fileInput.files && fileInput.files[0];
    if (!file) {
      setStatus("Chọn file để upload.", "warn");
      return;
    }
    const body = new FormData();
    body.append("file", file);
    body.append("title", file.name);
    try {
      setStatus(`Đang upload ${file.name}…`);
      const doc = await api(`/kb/${state.kbId}/documents`, {
        method: "POST",
        headers: headers(false),
        body,
      });
      const li = document.createElement("li");
      li.textContent = `${doc.title} · ${doc.parse_status} · ${doc.id.slice(0, 8)}…`;
      $("upload-log").prepend(li);
      e.target.reset();
      setStatus(`Upload xong — status: ${doc.parse_status}`);
    } catch (err) {
      setStatus(err.message, "error");
    }
  });

  // --- Chat / Agent ---
  $("form-chat").addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-mode]");
    if (btn) state.chatMode = btn.dataset.mode;
  });

  $("form-chat").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!state.kbId) {
      setStatus("Chọn KB có sẵn ở panel Knowledge để chat với dữ liệu cũ.", "warn");
      return;
    }
    const question = String(new FormData(e.target).get("question") || "").trim();
    $("answer-box").hidden = false;
    $("answer-text").textContent = "";
    $("citations").innerHTML = "";

    if (state.chatMode === "agent") {
      await runAgent(question);
    } else {
      await runChat(question);
    }
  });

  async function runChat(question) {
    try {
      setStatus("Đang chat…");
      const out = await api("/chat", {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ question, kb_id: state.kbId, top_k: 5 }),
      });
      $("answer-text").textContent = out.answer;
      for (const c of out.citations || []) {
        const li = document.createElement("li");
        li.innerHTML = `<strong>${escapeHtml(c.title)} · score ${Number(c.score).toFixed(3)}</strong>${escapeHtml(c.content)}`;
        $("citations").appendChild(li);
      }
      setStatus(`Chat xong · ${(out.citations || []).length} citation(s).`);
    } catch (err) {
      setStatus(err.message, "error");
    }
  }

  async function runAgent(question) {
    $("answer-text").textContent = "";
    setStatus("Agent SSE…");
    try {
      const res = await fetch("/agent/chat", {
        method: "POST",
        headers: headers(),
        body: JSON.stringify({ question, kb_id: state.kbId, max_steps: 5 }),
      });
      if (!res.ok) {
        const text = await res.text();
        let detail = text;
        try {
          detail = JSON.parse(text).detail || text;
        } catch {
          /* keep text */
        }
        throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";
      let answer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const parts = buffer.split("\n\n");
        buffer = parts.pop() || "";
        for (const block of parts) {
          handleSseBlock(block, (token) => {
            answer += token;
            $("answer-text").textContent = answer;
          });
        }
      }
      if (buffer.trim()) {
        handleSseBlock(buffer, (token) => {
          answer += token;
          $("answer-text").textContent = answer;
        });
      }
      setStatus("Agent done.");
    } catch (err) {
      setStatus(err.message, "error");
    }
  }

  function handleSseBlock(block, onToken) {
    const lines = block.split("\n");
    let event = "message";
    let data = "";
    for (const line of lines) {
      if (line.startsWith("event:")) event = line.slice(6).trim();
      else if (line.startsWith("data:")) data += line.slice(5).trim();
    }
    if (!data) return;
    let payload;
    try {
      payload = JSON.parse(data);
    } catch {
      payload = { raw: data };
    }
    const li = document.createElement("li");
    if (event === "token") {
      onToken(payload.text || "");
      return;
    }
    if (event === "done") {
      if (payload.answer) $("answer-text").textContent = payload.answer;
      li.innerHTML = `<strong>done</strong>${escapeHtml(JSON.stringify(payload))}`;
    } else if (event === "tool_result" && Array.isArray(payload.result)) {
      li.innerHTML = `<strong>${escapeHtml(event)} · ${escapeHtml(payload.tool || "")}</strong>${payload.result.length} hit(s)`;
      for (const hit of payload.result.slice(0, 3)) {
        const sub = document.createElement("li");
        sub.innerHTML = `<strong>${escapeHtml(hit.title || "doc")} · ${Number(hit.score || 0).toFixed(3)}</strong>${escapeHtml((hit.content || "").slice(0, 280))}`;
        $("citations").appendChild(sub);
      }
    } else {
      li.innerHTML = `<strong>${escapeHtml(event)}</strong>${escapeHtml(JSON.stringify(payload).slice(0, 400))}`;
    }
    $("citations").appendChild(li);
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  showViews();
  if (state.token) refreshMe();
  else setStatus("Chưa đăng nhập — dùng form bên trên.");
})();
